from flask import Flask, request, jsonify
from config.con_mongodb import con
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from functions.error import not_found
from functions.authUser import authenticate_user
from functions.generate_authtoken import generate_token
from dotenv import load_dotenv, dotenv_values
import os
load_dotenv()



app = Flask(__name__)

myClient = con();
myCol = myClient['Users']

#app.config['SECRET_KEY'] = 'AttendenceSystemWithSankalp@22co17Sahil@22co14Deepak@22co13'
securitykey = os.getenv("SECURITY_KEY")
app.config['SECRET_KEY'] = securitykey



@app.route('/')
def home():
    return "Hello World"


# route for post user data
@app.route('/signup', methods=['POST'])
def signup():
    try:
        _json = request.json
        name = _json['name']
        email = _json['email']
        password = _json['password']
        
        query = {'email': email}
        existing_document = myCol.find_one(query)
        if existing_document:
            resp = jsonify({'message': 'User already existing'})
            return resp
        else:
            hash_password = generate_password_hash(password,method='sha256')
            countD = myCol.count_documents({})
            token = generate_token(countD,app.config['SECRET_KEY'])
            myCol.insert_one({"_id":countD, "name": name, "email": email, "password": hash_password, "authtoken": token})
            resp = jsonify({'message': 'User registered successfully'})
            resp.status_code = 200
            return resp
    except:
        not_found
    
#route for get all users
@app.route('/getAllUsers',methods=['GET'])
def getAllData():
    try:
        users =  list(myCol.find())
        resp = jsonify(users)
        resp.status_code = 200
        return resp
    except:
        not_found
        
#rout for authenticating a user
@app.route('/signin', methods=['POST'])
def signin():
    _json = request.json
    email = _json.get('email')
    password = _json.get('password')
    auth = authenticate_user(myCol,email,password)
    return auth

#generating authtoken
# def generate_token(email):
#     # Get user information from the request (you may have a login process here)

#     # Validate the username and password (you can add your validation logic here)

#     # If validation is successful, create a JWT token
#     payload = {
#         'username': email,
#         'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)  # Token expiration time
#     }
#     token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
#     return jsonify({'token': token.decode('utf-8')})


if __name__ == "__main__":
    app.run(debug = True, port= 2700) 