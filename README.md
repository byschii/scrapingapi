# SIMPLE SCRAPING API

It's just an Uvicorn web server, which use FastAPI ho serve a simple API that retrives web pages with Playwright.

## Install

Run `pip install -r requirements.txt`, `playwright install-deps` and `playwright install`

## Setup

Change the default `DEFAULT_USER_KEY` in `user_utils.py`

## Serve

With `python ./main.py`

## Use 

You can run `requests.get( "http://localhost:8000/scrape", params={"url": LINK})`

### Simple Scraping Service

it also logs request by key

if no key is provided, default will be used

can block request from not listed keys

can create new key with a request to `new_user`
