// run in command line:
// npm i puppeteer

const puppeteer = require('puppeteer');

async function scrape() {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  await page.goto('https://usc.uva.nl/sport/groepsfitness/');
	await page.evaluate(()=>document.querySelector('#mod-schedule > div.schedule-select > div').click())
	await page.waitFor(1000);
	await page.setViewport({width: 1000, height: 1500})
	await page.screenshot({path: 'test.png'});
  await browser.close();
}
scrape().catch(console.error);
