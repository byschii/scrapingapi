
"""
user data are stored in json file
json is structured like
{
    "user_key": {
        "errors":0,
        "success":0},
    "next_key": {
        ...
        }
}
"""

import peewee
import random
import string
from datetime import datetime as dt
import enum

SCRAPER_DB = "scraper.db"
HEADER_KEY = "X-G3CPH-API-KEY"
DEFAULT_USER_KEY = "byschii"



db = peewee.SqliteDatabase(SCRAPER_DB)
class User(peewee.Model):
    """
    user model
    """
    user_key = peewee.CharField(unique=True)
    can_crate_new_user = peewee.BooleanField(default=False)

    class Meta:
        database = db

class Action(enum.Enum):
    """
    actions that can be performed on the user
    """
    CREATE_USER = "create_user"
    SCRAPE_URL = "scrape_url"
    PARSE_DOCUMENT = "parse_document"
    SUMMARIZE = "summarize"

class Log(peewee.Model):
    """
    log model
    """
    who = peewee.ForeignKeyField(User) 
    did = peewee.CharField(null=True) # action performed
    what = peewee.CharField(null=True) # url or user key
    when = peewee.DateTimeField(default=dt.now) 
    how = peewee.BooleanField(null=True) # True for success, False for error

    class Meta:
        database = db


db.connect()
db.create_tables([User, Log], safe=True)
u,c = User.get_or_create(user_key=DEFAULT_USER_KEY)



### USER CHECKS ###

def can_create_new_user(user_key:str):
    """
    check if the user can create a new user
    """
    u = User.get(User.user_key == user_key)
    return u.can_crate_new_user

def is_user_present(user_key:str):
    """
    check if user is present in the file
    """
    return user_key in [u.user_key for u in User.select()]

### LOGGING REQUESTS ###

def new_successfull_scrape(user_key:str, url:str):
    """
    log a new successfull request
    """
    Log.create(who=User.get(User.user_key == user_key), did=Action.SCRAPE_URL.value, what=url, how=True)

def new_failed_scrape(user_key:str, url:str):
    """
    log a new error request
    """
    Log.create(who=User.get(User.user_key == user_key), did=Action.SCRAPE_URL.value, what=url, how=False)

def new_successfull_parse(user_key:str, document:str):
    """
    log a new strip request
    """
    Log.create(who=User.get(User.user_key == user_key), did=Action.PARSE_DOCUMENT.value, what=document, how=True)

def new_failed_parse(user_key:str, document:str):
    """
    log a new strip request
    """
    Log.create(who=User.get(User.user_key == user_key), did=Action.PARSE_DOCUMENT.value, what=document, how=False)

def new_successfull_summarize(user_key:str, document:str):
    """
    log a new strip request
    """
    Log.create(who=User.get(User.user_key == user_key), did=Action.SUMMARIZE.value, what=document, how=True)

def new_failed_summarize(user_key:str, document:str):
    """
    log a new strip request
    """
    Log.create(who=User.get(User.user_key == user_key), did=Action.SUMMARIZE.value, what=document, how=False)



### USER GENERATION ###

def new_user(parent_key:str):
    """
    add a new user to the file
    """
    user_key = generate_new_api_key()
    User.create(user_key=user_key)
    Log.create(who=User.get(User.user_key == parent_key), did=Action.CREATE_USER.value, what=user_key, how=True)
    return user_key
    
def generate_new_api_key(lenght:int = 32):
    """generate a new random string"""
    key = "".join(random.choice(string.ascii_letters + string.digits) for _ in range(lenght))
    return key

