/**
 * Talking avatar from one still: a base image plus small pre-rendered cut-outs
 * (mouth shapes at 5 openings, eyelid and gaze steps). Every frame the player
 * reads the AI voice level, eases the mouth open and shut, picks a new mouth
 * shape at near-closed moments, blinks and glances on its own, and sways the
 * head a little. No video, no lip-sync model, no per-call cost.
 *
 * The atlas comes from make_atlas.py in the talking-avatar skill.
 */

export interface AvatarManifest {
  width: number;
  height: number;
  mouth: { x: number; y: number; levels: number; shapes: string[] };
  eyes: { x: number; y: number; levels: number; kinds: string[] };
}

export interface TalkingAvatarOptions {
  /** Folder holding manifest.json, base.webp, mouth/ and eyes/. */
  baseUrl: string;
  /** Current AI voice level (RMS, roughly 0..0.3). 0 when silent. */
  getLevel: () => number;
  /** Deprecated: sway is now drawn inside the canvas. */
  swayEl?: HTMLElement | null;
}

const SHAPE_WEIGHTS: Record<string, number> = { slight: 0.3, ah: 0.3, ee: 0.3, oo: 0.1 };

function load(src: string): Promise<HTMLImageElement> {
  return new Promise((resolve, reject) => {
    const img = new Image();
    img.onload = () => resolve(img);
    img.onerror = () => reject(new Error(`could not load ${src}`));
    img.src = src;
  });
}

function pickShape(shapes: string[], current: string): string {
  const options = shapes.filter((s) => s !== current);
  let r = Math.random() * options.reduce((n, s) => n + (SHAPE_WEIGHTS[s] ?? 0.2), 0);
  for (const s of options) {
    r -= SHAPE_WEIGHTS[s] ?? 0.2;
    if (r <= 0) return s;
  }
  return options[0] ?? current;
}

export async function startTalkingAvatar(canvas: HTMLCanvasElement, opts: TalkingAvatarOptions): Promise<() => void> {
  const root = opts.baseUrl.replace(/\/$/, '');
  const man = (await (await fetch(`${root}/manifest.json`)).json()) as AvatarManifest;
  const base = await load(`${root}/base.webp`);
  const mouth: Record<string, HTMLImageElement[]> = {};
  const eyes: Record<string, HTMLImageElement[]> = {};
  await Promise.all([
    ...man.mouth.shapes.map(async (s) => {
      mouth[s] = await Promise.all(Array.from({ length: man.mouth.levels }, (_, i) => load(`${root}/mouth/${s}-${i + 1}.webp`)));
    }),
    ...man.eyes.kinds.map(async (k) => {
      eyes[k] = await Promise.all(Array.from({ length: man.eyes.levels }, (_, i) => load(`${root}/eyes/${k}-${i + 1}.webp`)));
    }),
  ]);

  canvas.width = man.width;
  canvas.height = man.height;
  const ctx = canvas.getContext('2d');
  if (!ctx) throw new Error('no 2d context');

  let op = 0; // mouth openness 0..1
  let sv = 0; // smoothed draw level
  let shape = 'slight';
  let prevShape = 'slight';
  let switchedAt = 0;
  const recent: number[] = [];
  let nextBlink = performance.now() + 1500 + Math.random() * 2000;
  let blinkStart = -1;
  let glance: string | null = null;
  let glanceUntil = 0;
  let nextGlance = performance.now() + 3500 + Math.random() * 2000;
  let glanceAmt = 0;
  let nod = 0;
  let idleAmt = 1;
  const compCanvas = document.createElement('canvas');
  compCanvas.width = man.width;
  compCanvas.height = man.height;
  const comp = compCanvas.getContext('2d') as CanvasRenderingContext2D;
  const shapeLayerCanvas = document.createElement('canvas');
  shapeLayerCanvas.width = man.width;
  shapeLayerCanvas.height = man.height;
  const shapeLayer = shapeLayerCanvas.getContext('2d') as CanvasRenderingContext2D;
  let raf = 0;
  let last = 0;

  const frame = (now: number) => {
    raf = requestAnimationFrame(frame);
    if (now - last < 30) return; // ~30 fps
    last = now;
    const e = Math.max(0, opts.getLevel() || 0);
    recent.push(e);
    if (recent.length > 7) recent.shift();
    const local = Math.max(...recent, 1e-6);
    const voiced = e >= 0.01;

    // Openness follows loudness, with a syllable pulse; eases open and shut.
    const loud = voiced ? Math.min(1, 0.4 + 0.8 * Math.pow(e / 0.08, 0.8)) : 0;
    let target = loud * (0.2 + 0.8 * Math.pow(Math.min(1, e / local), 2));
    if (voiced) target = Math.max(target, 0.12);
    const step = target - op;
    op += Math.max(voiced ? -0.1 : -0.16, Math.min(0.15, step * (step > 0 ? 0.5 : 0.6)));
    // New shape at near-closed moments, or at least every ~200 ms while talking (cross-faded).
    const dip = e / local < 0.55;
    if ((op < 0.35 || dip || now - switchedAt > 160 + Math.random() * 120) && now - switchedAt > 90 && Math.random() < 0.6) {
      prevShape = shape;
      shape = pickShape(man.mouth.shapes, shape);
      switchedAt = now;
    }
    sv = sv * 0.55 + Math.min(1, op * 1.6) * 0.45;

    // Eyes: blink every ~2-5 s (sometimes twice), glance away in pauses.
    if (now >= nextBlink) {
      blinkStart = now;
      nextBlink = now + 2500 + Math.random() * 2500;
    }
    if (!voiced && now > 4000 && now >= nextGlance && now > glanceUntil) {
      glance = Math.random() < 0.5 ? 'lookL' : 'lookR';
      glanceUntil = now + 600 + Math.random() * 600;
      nextGlance = now + (voiced ? 4500 + Math.random() * 3000 : 2200 + Math.random() * 1800);
    }
    if (voiced) glanceUntil = Math.min(glanceUntil, now);
    glanceAmt += ((now < glanceUntil ? 1 : 0) - glanceAmt) * 0.2;

    // Compose the face (fractional blends between neighbouring steps, so nothing snaps).
    const c = comp;
    c.globalAlpha = 1;
    c.drawImage(base, 0, 0);
    const drawSteps = (frames: HTMLImageElement[], amt: number, x: number, y: number) => {
      const f = Math.max(0, Math.min(frames.length, amt * frames.length));
      const lo = Math.floor(f);
      const frac = f - lo;
      if (lo > 0) c.drawImage(frames[lo - 1], x, y);
      if (frac > 0.02 && lo < frames.length) {
        c.globalAlpha = frac;
        c.drawImage(frames[lo], x, y);
        c.globalAlpha = 1;
      }
    };
    if (sv > 0.01 && mouth[shape]) {
      const fade = Math.min(1, (now - switchedAt) / 120);
      if (fade < 1 && mouth[prevShape]) {
        drawSteps(mouth[prevShape], sv, man.mouth.x, man.mouth.y);
        // new shape over the old one at the same openness, faded in (no dip toward closed)
        const layer = shapeLayer;
        layer.clearRect(0, 0, man.width, man.height);
        const f = Math.max(0, Math.min(mouth[shape].length, sv * mouth[shape].length));
        const lo = Math.floor(f);
        if (lo > 0) layer.drawImage(mouth[shape][lo - 1], man.mouth.x, man.mouth.y);
        if (f - lo > 0.02 && lo < mouth[shape].length) { layer.globalAlpha = f - lo; layer.drawImage(mouth[shape][lo], man.mouth.x, man.mouth.y); layer.globalAlpha = 1; }
        c.globalAlpha = fade;
        c.drawImage(shapeLayerCanvas, 0, 0);
        c.globalAlpha = 1;
      } else drawSteps(mouth[shape], sv, man.mouth.x, man.mouth.y);
    }
    const bt = blinkStart < 0 ? -1 : (now - blinkStart) / 300;
    const blink = bt >= 0 && bt <= 1 ? (bt < 0.35 ? bt / 0.35 : bt < 0.55 ? 1 : 1 - (bt - 0.55) / 0.45) : 0;
    if (blink > 0.15 && eyes.blink) c.drawImage(eyes.blink[Math.min(eyes.blink.length, Math.max(1, Math.round(blink * eyes.blink.length))) - 1], man.eyes.x, man.eyes.y);
    else if (glanceAmt > 0.02 && glance && eyes[glance]) drawSteps(eyes[glance], glanceAmt * 0.85, man.eyes.x, man.eyes.y);

    // Head sway, breathing and a small nod with speech, drawn into the canvas (so recordings show it).
    nod += (op - nod) * 0.12;
    const t = now / 1000;
    idleAmt += ((voiced ? 0.6 : 1.2) - idleAmt) * 0.04;
    const ang = (1.1 * Math.sin((2 * Math.PI * t) / 5.3) + 0.4 * Math.sin((2 * Math.PI * t) / 2.3) + nod * 0.8) * (Math.PI / 180);
    const dx = idleAmt * 5 * Math.sin((2 * Math.PI * t) / 6.1);
    const dy = idleAmt * 3 * Math.sin((2 * Math.PI * t) / 3.7) + nod * 4 + 2.5 * Math.sin((2 * Math.PI * t) / 4.2);
    const sc = 1.04 + 0.004 * Math.sin((2 * Math.PI * t) / 4.0);
    const px = man.mouth.x + 110;
    const py = man.mouth.y + 230; // pivot near the neck
    ctx.setTransform(1, 0, 0, 1, 0, 0);
    ctx.translate(px + dx, py + dy);
    ctx.rotate(ang);
    ctx.scale(sc, sc);
    ctx.translate(-px, -py);
    ctx.drawImage(compCanvas, 0, 0);
    ctx.setTransform(1, 0, 0, 1, 0, 0);
  };
  raf = requestAnimationFrame(frame);
  return () => cancelAnimationFrame(raf);
}
