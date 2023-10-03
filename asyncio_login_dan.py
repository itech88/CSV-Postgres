from dotenv import load_dotenv, find_dotenv
import os
import asyncio
from playwright.async_api import async_playwright
import nest_asyncio
import icecream as ic
nest_asyncio.apply()
load_dotenv(find_dotenv())
# open the file containing the username
username = os.getenv("REVOLUTION_USERNAME")
password = os.getenv('REVOLUTION_PASSWORD')

# A dictionary to map the xpath of each field to its corresponding input data.
# This helps ensure that you always have the right data for each field.
# List of actions to be performed, in the order they should be executed.
actions = [         # put this into automation config file!!
{
    "name": "user",
    "group": "login",
    "type": "fill",
    "selector": "//*[@id='login-panel']/div/rev-login-form/div[2]/div/form/div[1]/div/input",
    "data": username
},
{
    "name": "password",
    "group": "login",
    "type": "fill",
    "selector": "//*[@id='login-panel']/div/rev-login-form/div[2]/div/form/div[2]/div/input",
    "data": password
},
{
    "name": "click",
    "group": "login",
    "type": "button",
    "selector": "//*[@id='login-panel']/div/rev-login-form/div[2]/div/form/button"
    # No "data" key here because it's a click action.
}, 
{
    "name": "report",
    "group": "login",
    "type": "button",
    "selector": '//*[@id="nav"]/li[8]/a'
},
{   
    "name": "patient",
    "group": "patient",
    "type": "button",
    "selector": '//*[@id="sidebar"]/pms-panel-menu/div/div[1]/div[1]/a' 
},
{
    "name": "patient_search",
    "group": "patient",
    "type": "button",
    "selector": '//*[@id="sidebar"]/pms-panel-menu/div/div[1]/div[2]/div/pms-panel-menu-sub/ul/li[1]/a'
},
{
    "name": "patient_address",
    "group": "patient",
    "type": "button",
    "selector": '//*[@id="main"]/pms-patient-search/pms-query-dashboard/div/div[2]/rev-ag-grid-container/ag-grid-angular/div/div[1]/div[2]/div[3]/div[2]/div/div/div[2]/div[4]/rev-template-cell-renderer/rev-button[1]/button'
},
{
    "name": "patient_address_export",
    "group": "patient",
    "type": "button",
    "selector": '//*[@id="sidebar"]/pms-panel-menu/div/div[3]/div[2]/div/pms-panel-menu-sub/ul/li[1]/a'
},
{
    "name": "accounting",
    "group": "accounting",
    "type": "button",
    "selector":
    '//*[@id="sidebar"]/pms-panel-menu/div/div[3]/div[1]/a'
},
{
    "name": "sales",
    "group": "accounting",
    "type": "button",
    "selector": '//*[@id="e-dropdown-btn-item_7"]'
},

{
    "name": "accounting_search",
    "group": "accounting",
    "type": "button",
    "selector": '//*[@id="main"]/pms-sales/div/div[2]/form/div[3]/div/button[1]'
}


]
    



async def main():
    # string_variable can be changed for different fields
    # this function can do all cases
    # can make another parameter that can do buttons
        

    async with async_playwright() as p:
        
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        await page.goto("https://revolutionehr.com/static/#/")

        for action in actions:
            selector = action["selector"]
            await page.wait_for_selector(selector)

            if action["type"] == 'fill': # and action['name'] == 'user'
                ic.ic(selector)
                ic.ic(action["data"])
                
                await page.fill(selector, action["data"])
                await page.wait_for_timeout(500) 

            # elif action["type"] == 'fill' and action['name'] == 'password':
            #     ic.ic(selector)
            #     ic.ic(action["data"])
                
            #     await page.fill(selector, action["data"])
            #     await page.wait_for_timeout(3000) 

            elif action["type"] == 'button':
                await page.click(selector)
                await page.wait_for_timeout(1000)

            else:
                print(f'Action type {action["type"]} not recognized')

        #await browser.close()
        page.sleep(1000000)

asyncio.run(main())




