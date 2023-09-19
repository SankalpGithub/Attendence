from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash


def authenticate_user(myCol,email,password):
    user = myCol.find_one({'email': email})
    
    if user:
        if check_password_hash(user['password'], password):
            resp = jsonify({'message': 'Authentication successful'})
            resp.status_code = 200
            return resp
        else:
            return jsonify({'message': 'Authentication failed (incorrect password)'})
    else:
        return jsonify({'message': 'Authentication failed (user not found)'})