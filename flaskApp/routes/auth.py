from flask import request, jsonify
from config.con_mongodb import con
from werkzeug.security import generate_password_hash, check_password_hash
from flaskApp.utils import generate_authtoken, send_gmail,timer
from dotenv import load_dotenv
import os
import threading
load_dotenv()





myClient = con();
myCol = myClient['Users']

securityKey = os.getenv('SECURITY_KEY')

#route to register user and send otp
def signup():
    try:
        _json = request.json
        name = _json.get('name')
        email = _json.get('email')
        password = _json.get('password')

        query = {'email': email}
        existing_document = myCol.find_one(query)
        if existing_document:
            resp = jsonify({'message': 'User already existing'})
            return resp
        else:
            sender_email = os.getenv("sender_email")
            gmailpassword = os.getenv("password")
            recipient_email = email
            otp = int(send_gmail.generate_otp())
            subject = 'Your OTP Code'
            body = f'Your OTP code is: {otp}'
            send = send_gmail.send_otp_email(sender_email, gmailpassword, recipient_email, subject, body)

            if send:
                hash_password = generate_password_hash(password,method='sha256')
                countD = myCol.count_documents({})
                # token = generate_authtoken.generate_token(countD,securitykey)
                myCol.insert_one({"_id": countD, "name": name, "email": email, "password": hash_password, "otp": otp, "isEmailVerify": False})
                print("starting timer")
                timer_thread = threading.Timer(120.00,checkVerify,args=(countD,None))
                timer_thread.start()
                resp =  jsonify({'message': 'OTP sent successfully!'})
                resp.status_code = 200
                return resp
            else:
                return jsonify({'message': 'Failed to send OTP'})
    except (ValueError, TypeError) as e:
    # Handle multiple exceptions
        resp = jsonify(f"Exception: {e}")
        return resp
    
def checkVerify(id,arg2):
    print("Starting...")
    user = myCol.find_one({'_id': id})
    if user['isEmailVerify']:
        print("user is verified")
    elif not user['isEmailVerify']:
        deleteUserbyId(id)
        
        
#route for virefy otp
def verifyOtp():
    try:
        _json = request.json
        email = _json.get('email')
        user_otp = _json.get('user_otp')
        query = {'email': email}
        user = myCol.find_one(query)

        if user['otp'] == user_otp:
            filter_criteria = {"_id": user['_id']}
            update_query = {"$unset": {"otp": 1},
                            "$set": {"isEmailVerify": True}}
            myCol.update_one(filter_criteria, update_query)
            resp = jsonify({'message': 'User Added successfully'})
            resp.status_code = 200
            return resp
        else:
            resp = jsonify({'message': 'OTP incorrect'})
            resp.status_code = 404
            return resp
    except (ValueError, TypeError) as e:
    # Handle multiple exceptions
        resp = jsonify(f"Exception: {e}")
        return resp
    
#route for get all users
def getAllData():
    try:
        users =  list(myCol.find())
        resp = jsonify(users)
        resp.status_code = 200
        return resp
    except (ValueError, TypeError) as e:
    # Handle multiple exceptions
        resp = jsonify(f"Exception: {e}")
        return resp
        
#rout for authenticating a user
def signin():
    try:
        _json = request.json
        email = _json.get('email')
        password = _json.get('password')
        user = myCol.find_one({'email': email})
        isEmailVerify = user['isEmailVerify']
        if user and isEmailVerify:
            if check_password_hash(user['password'], password):
                resp = jsonify({'message': 'Authentication successful'})
                resp.status_code = 200
                return resp
            else:
                return jsonify({'message': 'Authentication failed (incorrect password)'})
        elif not isEmailVerify:
            resp = jsonify({'message': 'Authentication failed (user is not verified)'})
            return resp
        else:
            return jsonify({'message': 'Authentication failed (user not found)'})
    except (ValueError, TypeError) as e:
    # Handle multiple exceptions
        resp = jsonify(f"Exception: {e}")
        return resp


#delete user by delete method
def deleteUserbyId(id):
    try:
        print("user deleted")
        if myCol.find_one({'_id': id}):
            # Delete the user with the custom ID
            myCol.delete_one({'_id': id})
            resp = jsonify({'message': 'User deleted successfully'})
            resp.status_code = 200
            return resp
        else:
            return jsonify({'message': 'User not found'}), 404

    except (ValueError, TypeError) as e:
    # Handle multiple exceptions
        resp = jsonify(f"Exception: {e}")
        return resp 

    
#route for reset password
def verify():
    try:
        token = request.args.get('token')
        data= generate_authtoken.decode_token(token,securityKey)
        id = data['id']
        password = data['password']
        user = myCol.find_one({'_id': id})
        isEmailVerify = user['isEmailVerify']
        if user and isEmailVerify:
            hash_password = generate_password_hash(password,method='sha256')
            filter_criteria = {"_id": id}
            update_query = {"$unset": {"token": 1},
                            "$set": {"password": hash_password}}
            myCol.update_one(filter_criteria, update_query)
            return jsonify({'message': 'Password reset successfully'}),200
        else:
            return jsonify({'message': 'User not found'})
    except (ValueError, TypeError) as e:
    # Handle multiple exceptions
        resp = jsonify(f"Exception: {e}"),404
        return resp
    
#route for reset password
def resetpassword():
    try:
        _json = request.json
        email = _json.get('email')
        password = _json.get('password')
        user = myCol.find_one({'email': email})
        if user and user['isEmailVerify']:
                token = generate_authtoken.generate_token(user['_id'],password,securityKey)
                print(token)
                filter_criteria = {"_id": user['_id']}
                update_query = {"$set": {"token": token}}
                myCol.update_one(filter_criteria, update_query)
                sender_email = os.getenv("sender_email")
                gmailpassword = os.getenv("password")
                recipient_email = email

                subject = 'Reset password'
                body = f'Click http://localhost:2700/verifyreset?token='+token+ ' to visit the link.'
                send = send_gmail.send_otp_email(sender_email, gmailpassword, recipient_email, subject, body)

                if send:
                    resp = jsonify({'message': 'Link sent successfully'})
                    resp.status_code = 200
                    return resp
                else:
                    return jsonify({'message': 'Failed to send Link'}), 404
        else:
            return jsonify({'message': 'User not found'})
    except (ValueError, TypeError) as e:
    # Handle multiple exceptions
        resp = jsonify(f"Exception: {e}"),404
        return resp
    
#route for resend otp
def resendotp():
    try:
        _json = request.json
        email = _json.get('email')
        user = myCol.find_one({'email': email})
        if user:
            sender_email = os.getenv("sender_email")
            gmailpassword = os.getenv("password")
            recipient_email = email
            otp = int(send_gmail.generate_otp())
            subject = 'Your OTP Code'
            body = f'Your OTP code is: {otp}'
            send = send_gmail.send_otp_email(sender_email, gmailpassword, recipient_email, subject, body)

            if send:
                filter_criteria = {"_id": user['_id']}
                update_query = {"$set": {"otp": otp}}
                myCol.update_one(filter_criteria, update_query)
                resp = jsonify({'message': 'OTP sent successfully!'})
                resp.status_code = 200
                return resp
            else:
                return jsonify({'message': 'Failed to send OTP'}), 404
        else:
            return jsonify({'message': 'User not found'}), 404
    except (ValueError, TypeError) as e:
    # Handle multiple exceptions
        resp = jsonify(f"Exception: {e}"),404
        return resp