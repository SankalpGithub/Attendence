from flask import request, jsonify, send_file
from config.con_mongodb import con
from flaskApp.utils import generate_authtoken, preseentOrAbsent
from dotenv import load_dotenv
import os
from openpyxl import Workbook
from io import BytesIO
load_dotenv()


securityKey = os.getenv('SECURITY_KEY')
myClient = con()
myCol = myClient['Users']
myColClass = myClient['Class']
myColLectures = myClient['lectures']

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
    
    
def getAllLectures():
    try:
        _json = request.json
        classId = _json.get('classId')
        result = myColLectures.find({'classId': classId})
        matching_documents = list(result)
        return jsonify(matching_documents)
    except (ValueError, TypeError) as e:
    # Handle multiple exceptions
        resp = jsonify(f"Exception: {e}")
        return resp
    

def getMyAttendence():
    try:
        _json = request.json
        classId = _json.get('classId')
        email = _json.get('email')
        myClass = myColClass.find_one({'_id': classId})
        user = myCol.find_one({'email': email})
        teacherId = myClass['userId']
        teacher = myCol.find_one({'_id': teacherId})
        userId = user['_id']
        className = myClass['className']
        name = teacher['name']
        result = myColLectures.find({'classId': classId})
        infoList = []
        for item in result:
            presentStudent = item['presentstudents']
            absentStudent = item['absentStudents']
            presentStatus = preseentOrAbsent.find_user_id(userId, presentStudent, absentStudent)
            data = {
            'presentStatus': presentStatus,
            'date': item['date'],
            'time': item['time'],
            'day': item['day']
            }
            infoList.append(data)
        postData = {
            'className': className,
            'Teacher': name,
            'infoList': infoList
        }
        return jsonify(postData)
    except (ValueError, TypeError) as e:
    # Handle multiple exceptions
        resp = jsonify(f"Exception: {e}")
        return resp
    
def getAllStudents():
    try:
        _json = request.json
        classId = _json.get('classId')
        myClass = myColClass.find_one({'_id': classId})
        joinStudents = myClass['joinedStudent']
        return jsonify(joinStudents)
    except (ValueError, TypeError) as e:
    # Handle multiple exceptions
        resp = jsonify(f"Exception: {e}")
        return resp
    
def classAttendence():
    try:
        _json = request.json
        lectureId = _json.get('lectureId')
        lecture = myColLectures.find_one({'_id': lectureId})
        if lecture['lectureStatus'] == 11:
            presentStudents = lecture['presentstudents']
            absentStudents = lecture['absentStudents']
            data = {
                'presentStudents': presentStudents,
                'absentStudents': absentStudents
            }
            resp = jsonify(data)
            resp.status_code = 200
            return resp
        else:
            resp = jsonify('Lecture is not completed yet')
            resp.status_code = 200
            return resp
    except (ValueError, TypeError) as e:
    # Handle multiple exceptions
        resp = jsonify(f"Exception: {e}")
        return resp
    
def export():
    _json = request.json
    lectureId = _json.get('lectureId')
    lecture = myColLectures.find_one({'_id': lectureId})
    data = {
        'absentStudents': lecture['absentStudents'],
        'presentStudents': lecture['presentstudents']
    }
    absent_students = data["absentStudents"]
    present_students = data["presentStudents"]

    # Create a single list containing all students marked as present or absent with name and email
    result_sequence = [(student["name"], student["email"], student["rollno"], "Present") for student in present_students] + \
                      [(student["name"], student["email"], student["rollno"], "Absent") for student in absent_students]

    # Sort the list by roll numbers
    sorted_result = sorted(result_sequence, key=lambda x: x[2])  # x[2] is the roll number



    data = sorted_result

    # Create a new Excel workbook
    workbook = Workbook()

    # Get the active sheet
    sheet = workbook.active

    # Set column headers
    sheet['A1'] = 'Name'
    sheet['B1'] = 'email'
    sheet['C1'] = 'rollno'
    sheet['D1'] = 'present Status'

    # Fill the Excel sheet with data
    for row_num, row_data in enumerate(data, start=2):
        for col_num, value in enumerate(row_data, start=1):
            sheet.cell(row=row_num, column=col_num, value=value)

    # Save the Excel file
    buffer = BytesIO()
    workbook.save(buffer)
    buffer.seek(0)

    # Send the Excel file as a response
    return send_file(buffer, as_attachment=True, download_name='student_data.xlsx', mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')


def exportlist():
    _json = request.json
    lectureId = _json.get('lectureId')
    lecture = myColLectures.find_one({'_id': lectureId})
    data = {
        'absentStudents': lecture['absentStudents'],
        'presentStudents': lecture['presentstudents']
    }
    absent_students = data["absentStudents"]
    present_students = data["presentStudents"]

    # Create a single list containing all students marked as present or absent with name and email
    result_sequence = [(student["name"], student["email"], student["rollno"], "Present") for student in present_students] + \
                      [(student["name"], student["email"], student["rollno"], "Absent") for student in absent_students]
                      
    return jsonify(result_sequence);