from flask import request, jsonify
from config.con_mongodb import con
from flaskApp.utils import dateTime,idGenerator,generate_authtoken
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
import os
load_dotenv()

myClient = con()
myCol = myClient['Users']
myColClass = myClient['Class']
myColLectures = myClient['lectures']
securityKey = os.getenv('SECURITY_KEY')

def createclass():
    try:
        _json = request.json
        className = _json.get('className')
        classPassword = _json.get('classPassword')
        # hash_classPassword = generate_password_hash(classPassword,method='sha256')
        authToken = request.headers.get('authToken')
        data = generate_authtoken.decode_token(authToken,securityKey)
        userId = data['id']
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
        
        
        myColClass.insert_one({'_id':id, 'className': className, 'classPassword': classPassword, 'userId': userId, 'generateCode': generateCode, 'date': date, 'day': day, 'time': time,
                               'joinedStudent': [], 'requested': [], 'takeClass': []})
        user = myCol.find_one({'_id': userId})
        isClass = myColClass.find_one({'_id': id})
        
    # Replace with the key-value pair you want to add
        numberOfStudents =  len(isClass.get("joinedStudent", []))
        data = {
            "classId": id,
            "className": className,
            "classPassword": classPassword,
            "numberOfStudents": numberOfStudents

        }
        update_query = {"$push": {"createClass": data}}
        # Perform the update
        myCol.update_one(user, update_query)
        resp = jsonify({'message': 'class created succcessfully', 'status': True})
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
        name = _json.get('name')
        rollno = _json.get('rollno')
        email = _json.get('email')
        classId = _json.get('classId')
        classPassword = _json.get('classPassword')
        authToken = request.headers.get('authToken')
        data = generate_authtoken.decode_token(authToken,securityKey)
        userId = data['id']
        isClass = myColClass.find_one({'_id': classId})
        joined = isClass['joinedStudent']
        user = myCol.find_one({'_id': userId})
        numberOfStudents =  len(joined)
        className = isClass['className']
        
        data = {
            'joinuserId': userId,
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
        requested = isClass['requested']
        # Perform the query
        foundINJoin = False
        foundInRequest = False

        for item in joinedStudent:
            if item.get("joinuserId") == userId:
                foundINJoin = True
                break
        
        for item in requested:
            if item.get("joinuserId") == userId:
                foundInRequest = True
                break

        if isClass:
            if not foundINJoin and  not foundInRequest:
                if isClass['classPassword'] == classPassword:
                    update_query = {"$push": {"requested": data}}
                    update_join = {"$push": {"joinedClass": joindata}}
                    # Perform the update
                    myColClass.update_one(isClass, update_query)
                    myCol.update_one(user, update_join)
                    resp = jsonify({'message': 'request sent to host', 'status': True})
                    resp.status_code = 200
                    return resp
                else:
                    resp = jsonify({'message': 'invalid information', 'status': False})
                    resp.status_code = 401
                    return resp
            elif foundINJoin:
                resp = jsonify({'messager': "You have allready joined the class", 'status': False})
                return resp
            elif foundInRequest:
                resp = jsonify({'messager': "You have sent request to host of the class", 'status': False})
                return resp
        else:
            return jsonify({'message': 'class not found', 'status': False})
            
        
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
        classId = _json.get('classId')
        email = _json.get('email')
        isAccepted = _json.get('isAccepted')
        user = myCol.find_one({'email': email})
        isClass = myColClass.find_one({'_id': classId})
        userId = user['_id']
        joined = isClass['joinedStudent']
        requested = isClass['requested']
        
        
        found_entry_request = None 
       
        for item in requested:
            if item.get("joinuserId") == userId:
                found_entry_request = item
                break
        
        
        data = {
            'userId': found_entry_request['joinuserId'],
            'name': found_entry_request['name'],
            'email': found_entry_request['email'],
            'rollno': found_entry_request['rollno'],
        }
        if isAccepted:
            update_join = {"$push": {"joinedStudent": data}}
            update_request ={ "$pull": { "requested": { "joinuserId": userId }}} 
            updated_query = {"$set": { "joinedClass.$.requestStatus": True}}
            
            # Perform the update
            myColClass.update_one(isClass, update_join)
            myColClass.update_one({"_id": classId}, update_request)
            myCol.update_one({"_id": userId, "joinedClass.classId": classId}, updated_query)
            
            numberOfStudents =  len(joined)
            updated_numberofS = { "$set": {"createClass.$.numberOfStudents": numberOfStudents }}
            updated_numberofs_join = { "$set": {"joinedClass.$.numberOfStudents": numberOfStudents }}
            
            myCol.update_one({"_id": userId}, updated_numberofS)
            myCol.update_one({"_id": userId, "joinedClass.classId": classId}, updated_numberofs_join)
            
            
            resp = jsonify({'message': 'request accepted'})
            resp.status_code = 200
            return resp
        else:
            update_request = {"$pull": {'requested': {"userId": userId}}}
            update_join = {"$pull": {'joinedClass': {"classId": classId}}}
            # Perform the update
            myColClass.update_one(isClass, update_request)
            myCol.update_one(user, update_join)
            resp = jsonify({'message': 'request rejected'})
            resp.status_code = 200
            return resp
    except (ValueError, TypeError) as e:
    # Handle multiple exceptions
        resp = jsonify(f"Exception: {e}")
        return resp
    
def deleteClassbyId(id):
    try:
        if myColClass.find_one({'_id': id}):
            isClass = myColClass.find_one({'_id': id})
            userId = isClass['userId']
            user = myCol.find_one({'_id': userId})
            # Delete the user with the custom ID
            myColClass.delete_one({'_id': id})
            update_request = {"$pull": {'requested': {"userId": userId}}}
            update_join = {"$pull": {'joinedClass': {"classId": id}}}
            update_created = {"$pull": {'createClass': {"classId": id}}}
            myColClass.update_one(isClass, update_request)
            myCol.update_one(user, update_join)
            myCol.update_one(user, update_created)
            resp = jsonify({'message': 'Class deleted successfully', 'status': True})
            resp.status_code = 200
            return resp
        else:
            return jsonify({'message': 'User not found', 'status': False}),404
    except (ValueError, TypeError) as e:
        # Handle multiple exceptions
        resp = jsonify(f"Exception: {e}")
        return resp 
    
    #starting lectures
    
def createLecture():
    try:
        _json = request.json
        classId = _json.get('classId')
        presentStudents = _json.get('presentStudents')
        absentStudents = _json.get('absentStudents')
        lectureStatus = _json.get('lectureStatus')
        datetime  = dateTime.daytime()
        date = datetime['date']
        day = datetime['day']
        time = datetime['time']
        isClass = myColClass.find_one({'_id': classId})
        countD = myColLectures.count_documents({})
        lectureData = {
            'lectureId': countD,
            'date': date,
            'day': day,
            'time': time,
            'lectureStatus': lectureStatus
            }
        if lectureStatus == 11:
            resp = jsonify({'message': f'lecture is uploded', 'status': True})
        elif lectureStatus == 10:
            resp = jsonify({'message': f'lecture is on hold', 'status': True})
        myColLectures.insert_one({'_id': countD, 'classId': classId, 'date': date, 'day': day, 'time': time, 'presentstudents': presentStudents, 'absentStudents': absentStudents, 'lectureStatus': lectureStatus})
        update_takeclass = {"$push": {"takeClass": lectureData}}
        myColClass.update_one(isClass, update_takeclass)
        resp.status_code = 200
        return resp
    except (ValueError, TypeError) as e:
        # Handle multiple exceptions
        resp = jsonify(f"Exception: {e}")
        return resp
        