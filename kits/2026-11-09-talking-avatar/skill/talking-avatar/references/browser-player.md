# Browser player: switch the avatar on the AI voice

Read at step 4. Both versions do the same thing: measure the AI audio, show the
talking asset while it is above a threshold, hold it through short gaps, and
fall back to the still portrait if a clip fails.

## 1. Measure the AI voice level (any framework)

Attach this to the remote audio stream (WebRTC `ontrack`, or an `<audio>` element
via `ctx.createMediaElementSource`).

```js
function createLevelMeter(stream) {
  const ctx = new AudioContext();
  const src = ctx.createMediaStreamSource(stream);
  const an = ctx.createAnalyser(); an.fftSize = 1024; src.connect(an);
  const buf = new Float32Array(an.fftSize);
  return {
    read() { an.getFloatTimeDomainData(buf); let s = 0; for (const v of buf) s += v * v; return Math.sqrt(s / buf.length); },
    close() { ctx.close(); },
  };
}
// Poll every 100 ms; speaking = level > 0.01 (tune for your audio).
```

If the voice is TTS you play yourself, you can also flip `speaking` on the
audio element's `play`/`ended` events instead of measuring.

## 2. React component (Tailwind classes; adapt to your styling)

```tsx
'use client';
import { useEffect, useState } from 'react';

const SILENCE_MS = 400; // keep talking through short gaps between words
const A = { still: '/avatar.jpg', idle: '/avatar-idle.mp4', talk: '/avatar-talk.mp4', poster: '/avatar-poster.jpg' };

export default function TalkingPortrait({ speaking, alt }: { speaking: boolean; alt: string }) {
  const [talking, setTalking] = useState(false);
  const [failed, setFailed] = useState(false);
  useEffect(() => {
    if (speaking) { setTalking(true); return; }
    const t = window.setTimeout(() => setTalking(false), SILENCE_MS);
    return () => window.clearTimeout(t);
  }, [speaking]);
  if (failed) return <img src={A.still} alt={alt} className="absolute inset-0 w-full h-full object-cover" />;
  const video = (src: string, visible: boolean) => (
    <video src={src} poster={A.poster} autoPlay loop muted playsInline preload="auto"
      aria-hidden={!visible} onError={() => setFailed(true)}
      className={`absolute inset-0 w-full h-full object-cover transition-opacity duration-200 ${visible ? 'opacity-100' : 'opacity-0'}`} />
  );
  return (
    <div role="img" aria-label={alt} className="absolute inset-0">
      {video(A.idle, !talking)}
      {video(A.talk, talking)}
    </div>
  );
}
```

Both videos play all the time; only opacity changes. That makes the switch
instant (no seek, no buffering) and is why both must be `muted` (autoplay rule).

## 3. Plain JS (no framework)

```html
<div class="avatar" style="position:relative;aspect-ratio:16/9;overflow:hidden">
  <video id="idle" src="avatar-idle.mp4" poster="avatar-poster.jpg" autoplay loop muted playsinline style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;transition:opacity .2s"></video>
  <video id="talk" src="avatar-talk.mp4" autoplay loop muted playsinline style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:0;transition:opacity .2s"></video>
</div>
<script>
  let quietSince = 0;
  function setSpeaking(on) {            // call every 100 ms with level > 0.01
    const now = performance.now();
    if (on) quietSince = 0; else if (!quietSince) quietSince = now;
    const talking = on || now - quietSince < 400;
    talk.style.opacity = talking ? 1 : 0; idle.style.opacity = talking ? 0 : 1;
  }
</script>
```

## 4. Stills flipbook variant (fallback assets)

When you have stills instead of clips (step 2 fallback, untested in production), stack 3-4 `<img>`s
(mouth closed, half open, open; optional blink) and every 80-120 ms while
talking show one chosen by level: < 0.02 closed, < 0.05 half, else open, with a
little randomness so it does not look mechanical. While listening, show closed
and swap to the blink frame for 150 ms every 3-6 s. Preload all stills.
