const { chromium } = require('playwright'); const fs = require('fs');
(async () => {
  const b = await chromium.launch({ channel: 'chrome', args: ['--autoplay-policy=no-user-gesture-required'] });
  const p = await (await b.newContext({ viewport: { width: 1300, height: 740 } })).newPage();
  p.on('console', (m) => console.log('[page]', m.text()));
  await p.goto('http://127.0.0.1:8766/index.html');
  const b64 = await p.evaluate(() => window.run());
  fs.writeFileSync(process.argv[2], Buffer.from(b64, 'base64')); await b.close(); console.log('ok');
})();
