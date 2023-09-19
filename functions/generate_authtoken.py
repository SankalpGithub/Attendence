from flask import Flask, request, jsonify
import jwt
import datetime



def generate_token(id,securitykey):
    # Get user information from the request (you may have a login process here)


    # Validate the username and password (you can add your validation logic here)

    # If validation is successful, create a JWT token
    
    payload = {
            'id': id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)  # Token expiration time
    }
    token = jwt.encode(payload,securitykey, algorithm='HS256')
    return token
