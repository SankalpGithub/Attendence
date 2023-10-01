from flask import request, jsonify
from config.con_mongodb import con

myClient = con()
myCol = myClient['Users']

#https://takemyattendence-27rl.onrender.com/

def getUserById(id):
    try:
        user = myCol.find_one({'_id': id})
        print(user)
        resp = jsonify(user)
        resp.status_code = 200
        return resp
    except (ValueError, TypeError) as e:
    # Handle multiple exceptions
        resp = jsonify(f"Exception: {e}")
        return resp
