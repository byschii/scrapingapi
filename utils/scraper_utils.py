
from playwright.sync_api import sync_playwright

import time 

# for proxy
# browser = await chromium.launch(proxy={
#  "server": "http://myproxy.com:3128",
# with ip from https://vpnoverview.com/privacy/anonymous-browsing/free-proxy-servers/

def run_scrape(page_url:str, max_wait:int=10, sleep_time:int=7) -> str:
    with sync_playwright() as playwright:
        # launch the browser
        browser = playwright.chromium.launch()
        page = browser.new_page()
        # sets timeout for the page
        page.set_default_timeout(int(max_wait*1_000))
        # gets the page fron the url
        page.goto(page_url)
        # wait for the page to load
        page.wait_for_selector("body")
        # wait 7sec for the page to load
        time.sleep(sleep_time)
        # scroll to the bottom of the page
        page.evaluate("() => window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(sleep_time/2)
        page.evaluate("() => window.scrollTo(0, document.body.scrollHeight)")
        # get the page content and close the browser
        content = page.content()
        browser.close()
    return content





