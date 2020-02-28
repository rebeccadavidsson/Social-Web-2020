// Instal node.js
// run in command line IN THIS FOLDER!!!:
//    npm install puppeteer@2.0.0
// then run:
//    node scraper.js

// 1 = ASC, 2 = AmstelCampus, 3 = CREA, 4 = ClubWest, 5 = Universum
const fs = require('fs')

function scraper(loc) {

  const puppeteer = require('puppeteer');

  // Viewport && Window size
  const width = 600
  const height = 800

  async function scrape() {
    const browser = await puppeteer.launch({
        headless: false,
        args: [`--window-size=${width},${height}`]
      }); // default is true
    const page = await browser.newPage();
    await page.goto('https://usc.uva.nl/sport/groepsfitness/');
  	await page.evaluate(()=>document.querySelector('#mod-schedule > div.schedule-select > div').click())

    // Wait a while until loaded
    await page.waitFor(1000);

    // Click on location
    await page.evaluate((loc) => {
      document.querySelector('#mod-schedule > div.schedule-select.s-active > ul > li:nth-child(' + loc + ')').click()
    }, loc);

    await page.waitFor(1000);
    await page.evaluate(()=>document.querySelector('#schedule-cont > ul > li.current').click())

    // DUURT SUPER LANG HOLY SHIT
    await page.waitFor(5000);
    var inner_html = await page.evaluate(() => document.querySelector('#schedule-cont > div').innerHTML);

    // Click on next week
  	await page.evaluate(()=>document.querySelector('#schedule-cont > ul > li.next').click())

    await page.waitFor(5000);
    inner_html += await page.evaluate(() => document.querySelector('#schedule-cont > div').innerHTML);

    // Write data in 'Output.txt' .
    fs.writeFile('converter/templates/output.html', inner_html, (err) => {

        // In case of a error throw err.
        if (err) throw err;
    })


    await browser.close();
    return inner_html
  }
  scrape().catch(console.error);
}

result = scraper(5)

return result
