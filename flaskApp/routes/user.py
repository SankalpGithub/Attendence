from flask import request, jsonify
from config.con_mongodb import con
from flaskApp.utils import generate_authtoken
from dotenv import load_dotenv
import os
load_dotenv()


securityKey = os.getenv('SECURITY_KEY')
myClient = con()
myCol = myClient['Users']

#https://takemyattendence-27rl.onrender.com/

def getUserById():
    try:
        authToken = request.headers.get('authToken')
        authData = generate_authtoken.decode_token(authToken,securityKey)
        userId = authData['id']
        user = myCol.find_one({'_id': userId})
        data = {
            'name': user['name'],
            'createClass': user['createClass'],
            'email': user['email'],
            'joinedClass': user['joinedClass']
        }
        resp = jsonify(data)
        resp.status_code = 200
        return resp
    except (ValueError, TypeError) as e:
    # Handle multiple exceptions
        resp = jsonify(f"Exception: {e}")
        return resp
    
    
def getjoinedStudents():
    try:
        authToken = request.headers.get('authToken')
        authData = generate_authtoken.decode_token(authToken,securityKey)
        userId = authData['id']
    except (ValueError, TypeError) as e:
    # Handle multiple exceptions
        resp = jsonify(f"Exception: {e}")
        return resp