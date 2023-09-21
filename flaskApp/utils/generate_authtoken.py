
import jwt




def generate_token(id,password,securitykey): 
    payload = {
            'id': id,
            'password': password
    }
    token = jwt.encode(payload,securitykey, algorithm='HS256')
    return token

def decode_token(token,securitykey):

    try:
        payload = jwt.decode(token,securitykey, algorithms=['HS256'])
        data = {
        'password': payload['id'],
        'email': payload['email']    
        }   
        return data
    except jwt.ExpiredSignatureError:
        return {'message': 'Token has expired'},401
    except jwt.InvalidTokenError:
        return {'message': 'Invalid token'},401
