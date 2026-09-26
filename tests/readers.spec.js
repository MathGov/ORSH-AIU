const {test,expect}=require('@playwright/test');
const AxeBuilder=require('@axe-core/playwright').default;
const docs=require('../papers.json');
for(const d of docs){test(d.title+': equations, navigation and accessibility',async({page})=>{
 await page.goto('/read/'+d.slug+'.html');await page.waitForFunction(()=>document.documentElement.dataset.mathReady==='true');
 await page.evaluate(()=>document.fonts.ready);
 expect(await page.locator('.katex-error').count()).toBe(0);
 expect(await page.locator('.katex').count()).toBeGreaterThan(0);
 for(const width of [320,390,768,1280]){await page.setViewportSize({width,height:900});expect(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1)).toBe(true);}
 const results=await new AxeBuilder({page}).withTags(['wcag2a','wcag2aa','wcag21aa']).analyze();expect(results.violations).toEqual([]);
 const link=page.locator('nav[aria-label="Paper contents"] a').nth(2);const href=await link.getAttribute('href');await link.click();expect(new URL(page.url()).hash).toBe(href);
});}
test('home and guides are accessible at mobile size',async({page})=>{
 await page.setViewportSize({width:390,height:844});
 for(const url of ['/','/downloads.html','/reproduce.html','/cite.html','/license.html','/evidence.html','/search.html']){await page.goto(url);expect(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1)).toBe(true);const results=await new AxeBuilder({page}).withTags(['wcag2a','wcag2aa','wcag21aa']).analyze();expect(results.violations).toEqual([]);}
});
test('search finds an anchored scientific passage and handles a retry',async({page})=>{
 await page.goto('/search.html');await page.route('**/search-index.json',route=>route.abort());await page.locator('#query').fill('conditional typicality');await page.getByRole('button',{name:'Search',exact:true}).click();await expect(page.locator('#status')).toContainText('retry');await page.unroute('**/search-index.json');await page.locator('#scope').selectOption('frame-aligned-records');await page.getByRole('button',{name:'Search',exact:true}).click();await expect(page.locator('#results article').first()).toBeVisible();await page.locator('#results a').first().click();await expect(page.locator(':target')).toBeVisible();
});
