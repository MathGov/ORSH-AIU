const {defineConfig}=require('@playwright/test');
module.exports=defineConfig({testDir:'./tests',timeout:90000,workers:2,use:{baseURL:'http://127.0.0.1:4174',browserName:'chromium',channel:process.env.PLAYWRIGHT_CHANNEL||undefined},webServer:{command:'node scripts/serve_site.js',port:4174,reuseExistingServer:false},reporter:'list'});
