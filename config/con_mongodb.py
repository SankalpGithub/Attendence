import os
import pymongo
from dotenv import load_dotenv, dotenv_values

load_dotenv()

def con():
    try:
        myclient = pymongo.MongoClient(os.getenv("connString"))
        return myclient["Attendence"]
    except:
        return "Error Connecting Database"