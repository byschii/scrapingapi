
"""
This is a simple server that use FastAPI and Plawwright help with web scraping
"""
import argparse
import logging
from validator_collection import validators, checkers
from validator_collection.errors import InvalidURLError
import random
import string
import time

import utils.scraper_utils as scraper_utils
import utils.user_utils as user_utils
from request_models import ScrapeRequest
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import uvicorn

app = FastAPI()
apiv1_prefix = "" #apiv1_prefix = "/api/v1"
CONFIG_FILE = './secret.ini'
CHECK_USER = False


parser = argparse.ArgumentParser()
parser.add_argument("-b", "--broadcast", 
    help="switch from localhost to all interfaces", 
    default=False, action='store_true')


@app.middleware("http")
async def is_valid_header_key(request: Request, call_next):
    """
    check if the header key is valid and update last request time
    """
    key = request.headers.get(user_utils.HEADER_KEY)
    
    bad_key = key is None or user_utils.is_user_present(key) == False
    api_requested = request.url.path.startswith(apiv1_prefix)

    if (api_requested and bad_key) and CHECK_USER:
        return JSONResponse(status_code=403, content={"error": f"Invalid header key: {key}"})
    else:
        return await call_next(request)




@app.post(f"{apiv1_prefix}/new_user")
async def new_user(request: Request):
    """
    create a new user
    """
    if user_utils.can_create_new_user( request.headers.get(user_utils.HEADER_KEY) ) is False:
        return JSONResponse(status_code=403, content={"error": "Can't create new user"})
    else:
        key = user_utils.new_user(key)
        return JSONResponse(content={"key": key, "message": f"use the key in the {user_utils.HEADER_KEY} header"})


@app.post(f"{apiv1_prefix}/scrape")
def scrape(request:Request, data: ScrapeRequest):
    """
    page_url: str - the url of the page to scrape
    max_wait: int - the maximum time in seconds to wait for the page to load, pass 0 to disable timeout
    """
    user_key = request.headers.get(user_utils.HEADER_KEY) or user_utils.DEFAULT_USER_KEY
    try:
        validators.url(data.url)
        content = scraper_utils.run_scrape(data.url, data.max_wait)
        user_utils.new_successfull_scrape(user_key, data.url)
        return JSONResponse(status_code=200, content={ "page": content })
    except InvalidURLError as e:
        user_utils.new_failed_scrape(user_key, data.url)
        return JSONResponse(status_code=400, content={ "error": str(e) })
    except Exception as e:
        user_utils.new_failed_scrape(user_key, data.url)
        return JSONResponse(status_code=500, content={ "error": str(e) })
      
      

    

if __name__ == "__main__":
    args = parser.parse_args()
    address = "0.0.0.0" if args.broadcast else "127.0.0.1"

    uvicorn.run(
        app, host=address, port=8000
    )

