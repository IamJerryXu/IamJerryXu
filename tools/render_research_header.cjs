/* Rasterize the composed SVG layout for a lightweight GitHub image.
   Run after build_research_header.py, with Playwright available in NODE_PATH. */
const {chromium} = require('playwright');
const fs = require('fs');
const path = require('path');
(async () => {
  const browser = await chromium.launch({headless:true, ...(process.env.CHROME_PATH ? {executablePath:process.env.CHROME_PATH} : {})});
  for (const [name,width,height] of [['research-header-v4',1200,300],['research-header-mobile-v4',600,250]]) {
    const svg = path.join(__dirname,'..','assets',name+'.svg');
    const page = await browser.newPage({viewport:{width,height}, deviceScaleFactor:2});
    await page.setContent('<style>body{margin:0}svg{display:block}</style>'+fs.readFileSync(svg,'utf8'));
    await page.evaluate(async () => {
      await Promise.all([document.fonts.load('700 68px Pagella'), document.fonts.load('400 23px Pagella')]);
      await document.fonts.ready;
      await Promise.all([...document.images].map(i => i.decode()));
    });
    await page.screenshot({path:svg.replace(/\.svg$/,'.png'),omitBackground:true});
    await page.close();
    fs.unlinkSync(svg);
  }
  await browser.close();
})();
