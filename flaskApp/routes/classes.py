from flask import request, jsonify
from config.con_mongodb import con
from flaskApp.utils import dateTime

myClient = con();
myCol = myClient['Users']
myColClass = myClient['Class']


def createclass():
    try:
        _json = request.json
        className = _json.get('className')
        classPassword = _json.get('classPassword')
        userId = _json.get('userId')
        
        
        id = 1234567893
        datetime  = dateTime.daytime()
        date = datetime['date']
        day = datetime['day']
        time = datetime['time']
        # count = myColClass.count_documents({'joinedClass': id})
        
        
        myColClass.insert_one({'_id':id, 'className': className, 'classPassword': classPassword, 'userId': userId, 'generateCode': "#12365", 'date': date, 'day': day, 'time': time,
                               'joinedStudent': [], 'requested': [], 'takeClass': []})
        user = myCol.find_one({'_id': userId}) # Replace with the key-value pair you want to add
        update_query = {"$push": {"createClass": id}}
        # Perform the update
        myCol.update_one(user, update_query)
        print("class created succcessfully")
        return jsonify({'message': 'class created succcessfully'})
    
    except (ValueError, TypeError) as e:
    # Handle multiple exceptions
        resp = jsonify(f"Exception: {e}")
        return resp

def getAllClasses():
    try:
        users =  list(myColClass.find())
        resp = jsonify(users)
        resp.status_code = 200
        return resp
    except (ValueError, TypeError) as e:
    # Handle multiple exceptions
        resp = jsonify(f"Exception: {e}")
        return resp

def joinClass():
    try:
        _json = request.json
        userId = _json.get('UserId')
        name = _json.get('name')
        rollno = _json.get('rollno')
        classId = _json.get('classId')
        classPassword = _json.get('classPassword')
        data = {
            'userId': userId,
            'name': name,
            'rollno': rollno,
        }
        isClass = myColClass.find_one({'_id': classId})
        if isClass:
            update_query = {"$push": {"requested": [data]}}
            # Perform the update
            myCol.update_one(isClass, update_query)
            return jsonify({'message': 'request sent to host'})
        else:
            return jsonify({'message': 'class not found'})  
            
        
    except (ValueError, TypeError) as e:
    # Handle multiple exceptions
        resp = jsonify(f"Exception: {e}")
        return resp