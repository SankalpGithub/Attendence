from flask import request, jsonify
from config.con_mongodb import con
from flaskApp.utils import dateTime,idGenerator
from werkzeug.security import generate_password_hash, check_password_hash

myClient = con()
myCol = myClient['Users']
myColClass = myClient['Class']


def createclass():
    try:
        _json = request.json
        className = _json.get('className')
        classPassword = _json.get('classPassword')
        userId = _json.get('userId')
        hash_classPassword = generate_password_hash(classPassword,method='sha256')
        
        id = 0
        datetime  = dateTime.daytime()
        date = datetime['date']
        day = datetime['day']
        time = datetime['time']
        
        isId = True
        while isId:
            id = idGenerator.idgen()
            if not myColClass.find_one({'_id': id}):
                isId = False
            else:
                isId = True
                
        generateCode = ""
        isCode = True
        while isCode: 
            generateCode = idGenerator.codeGenerator()
            if not myColClass.find_one({'generateCode': generateCode}):
                isCode = False
            else:
                isCode = True
        
        
        myColClass.insert_one({'_id':id, 'className': className, 'classPassword': hash_classPassword, 'userId': userId, 'generateCode': generateCode, 'date': date, 'day': day, 'time': time,
                               'joinedStudent': [], 'requested': [], 'takeClass': []})
        user = myCol.find_one({'_id': userId})
        
    # Replace with the key-value pair you want to add
        numberOfStudents =  len(user.get("joinedStudent", []))
        data = {
            "classId": id,
            "className": className,
            "numberOfStudents": numberOfStudents

        }
        update_query = {"$push": {"createClass": data}}
        # Perform the update
        myCol.update_one(user, update_query)
        resp = jsonify({'message': 'class created succcessfully'})
        resp.status_code = 200
        return resp
    
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
        email = _json.get('email')
        classId = _json.get('classId')
        classPassword = _json.get('classPassword')
        isClass = myColClass.find_one({'_id': classId})
        user = myCol.find_one({'_id': userId})
        numberOfStudents =  len(user.get("joinedStudent", []))
        className = isClass['className']
        
        data = {
            'userId': userId,
            'name': name,
            'email': email,
            'rollno': rollno,
        }
        joindata = {
            "classId": classId,
            "className": className,
            "numberOfStudents": numberOfStudents,
            "requestStatus": False
        }
        
        joinedStudent = isClass['joinedStudent']
        print(joinedStudent)
        requested = isClass['requested']
        # Perform the query
        foundINJoin = False
        foundInRequest = False

        for item in joinedStudent:
            if item.get("userId") == userId:
                foundINJoin = True
                break
        
        for item in requested:
            if item.get("userId") == userId:
                foundInRequest = True
                break

        print(joinedStudent)
        
        # requestresult = myColClass.find({requested: userId})
        print(requested)
        if isClass:
            if not foundINJoin and  not foundInRequest:
                if check_password_hash(isClass['classPassword'], classPassword):
                    update_query = {"$push": {"requested": data}}
                    update_join = {"$push": {"joinedClass": joindata}}
                    # Perform the update
                    myColClass.update_one(isClass, update_query)
                    myCol.update_one(user, update_join)
                    resp = jsonify({'message': 'request sent to host'})
                    resp.status_code = 200
                    return resp
                else:
                    resp = jsonify({'message': 'invalid information'})
                    resp.status_code = 401
                    return resp
            elif foundINJoin:
                resp = jsonify("You have allready joined the class")
                return resp
            elif foundInRequest:
                resp = jsonify("You have sent request to host of the class")
                return resp
        else:
            return jsonify({'message': 'class not found'})
            
        
    except (ValueError, TypeError) as e:
    # Handle multiple exceptions
        resp = jsonify(f"Exception: {e}")
        return resp
    

def allRequests():
    try:
        _json = request.json
        classId = _json.get('classId')
        myclass = myColClass.find_one({'_id': classId})
        requestStudents = myclass['requested']
        resp = jsonify(requestStudents)
        resp.status_code = 200
        return resp
    except (ValueError, TypeError) as e:
    # Handle multiple exceptions
        resp = jsonify(f"Exception: {e}")
        return resp
    
def acceptrequest():
    try:
        _json = request.json
        userId = _json.get('userId')
        classId = _json.get('classId')
        isAccepted = _json.get('isAccepted')
        user = myCol.find_one({'_id': userId})
        joined = user['joinedClass']
        print(joined)
        
        isClass = myColClass.find_one({'_id': classId})
        print(isClass)
        requested = isClass['requested']
        print(requested)
        
        
        found_entry = None

        for item in requested:
            if item.get("userId") == userId:
                found_entry = item
                break
        
        found_joinEntry = None

        for item in joined:
            if item.get("classId") == classId:
                found_joinEntry = item
                break
            
        data = {
            'userId': found_entry['userId'],
            'name': found_entry['name'],
            'email': found_entry['email'],
            'rollno': found_entry['rollno'],
        }
        if isAccepted:
            updated_query = {"$push": {"requestStatus": True}}
            update_join = {"$push": {"joinedStudent": data}}
            update_request = {"$pull": {'requested': {"userId": userId}}}
            # Perform the update
            myCol.update_one(user, updated_query)
            myCol.update_one(isClass, update_join)
            myCol.update_one(isClass, update_request)
            resp = jsonify({'message': 'request accepted'})
            resp.status_code = 200
            return resp
        else:
            update_request = {"$pull": {'requested': {"userId": userId}}}
            update_join = {"$pull": {'joinedClass': {"classId": classId}}}
            # Perform the update
            myColClass.update_one(isClass, update_request)
            myColClass.update_one(user, update_join)
            resp = jsonify({'message': 'request rejected'})
            resp.status_code = 200
            return resp
    except (ValueError, TypeError) as e:
    # Handle multiple exceptions
        resp = jsonify(f"Exception: {e}")
        return resp