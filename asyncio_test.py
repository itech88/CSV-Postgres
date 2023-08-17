import asyncio
from playwright.async_api import async_playwright
import nest_asyncio
nest_asyncio.apply()

# string_variable can be changed for different fields
# this function can do all cases
# can make another parameter that can do buttons

# all the actions in the html
array = ['fill', 'click button', 'select dropdown', 'select date']
xpath = {'user_login': '//*[@id="login-panel"]/div/rev-login-form/div[2]/div/form/div[1]/div/input',
         'password_login': 'password'}

async def main(field, type_of_method):
    async with async_playwright() as p:
        
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto("https://revolutionehr.com/static/#/")

        selector = field
        #
        await page.wait_for_selector(selector)
        element = await page.query_selector(selector)

        if type_of_method == 'fill':
            if element:
            #print(await element.inner_text())
                await element.fill("mbakerod")    
                await page.wait_for_timeout(3000)  # Time is in milliseconds     
        elif type_of_method == 'click button':
            pass
            #insert code for clicking button
                
        else:
            print('Element not found')

        

        await browser.close()

# insert the xpath and the action array
asyncio.run(main(xpath('user_login'), 'fill'))
