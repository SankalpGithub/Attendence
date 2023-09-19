import os
import pymongo
from dotenv import load_dotenv, dotenv_values

load_dotenv()

def con():
    try:
        myclient = pymongo.MongoClient(os.getenv("connString"))
        print("MongoDB connected successfully")
        return myclient["Attendence"]
    except:
        print("Error Connecting Database")