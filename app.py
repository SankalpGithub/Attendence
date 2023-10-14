from flask import Flask
from config.con_mongodb import con
from flaskApp.routes import auth,classes,user

app = Flask(__name__)

from flask_cors import CORS

# Configure CORS to allow requests from all origins
cors = CORS(app)



# myClient = con();
# myCol = myClient['Users']


# securitykey = os.getenv("SECURITY_KEY")
# app.config['SECRET_KEY'] = securitykey




# # route for post user data
@app.route('/signup', methods=['POST'])
def signup():
        return auth.signup()         
    

        
#route for add user
@app.route('/verifyEmail', methods=['POST'])
def verifyOtp():
    return auth.verifyOtp()

    
#route for get all users
@app.route('/',methods=['GET'])
def getAllData():
    return auth.getAllData()

        
#rout for authenticating a user
@app.route('/signin', methods=['POST'])
def signin():
    return auth.signin()


#delete user by delete method
@app.route('/deleteUser/<int:id>', methods=['DELETE'])
def deleteUserbyId(id):
    return auth.deleteUserbyId(id)
  
    
    
#route to send reset password page link
@app.route('/resetpassword', methods=['POST'])
def resetpassword():
    return auth.resetpassword()

@app.route('/verifyreset', methods=['GET'])
def verifyreset():
    return auth.verify()

@app.route('/resendotp', methods=['POST'])
def resendotp():
    return auth.resendotp()


@app.route('/createClass', methods=['POST'])
def createClass():
    return classes.createclass()

@app.route('/getAllClasses',methods=['GET'])
def getAllClasses():
    return classes.getAllClasses()


@app.route('/joinClass',methods=['POST'])
def joinClass():
    return classes.joinClass()


@app.route('/user',methods=['GET'])
def getUserById():
    return user.getUserById()


@app.route('/allRequest',methods=['POST'])
def allRequest():
    return classes.allRequests()


@app.route('/acceptrequest',methods=['POST'])
def acceptrequest():
    return classes.acceptrequest()

@app.route('/deleteclass/<int:id>', methods=['DELETE'])
def deleteClassbyId(id):
    return classes.deleteClassbyId(id)

@app.route('/createLecture',methods=['POST'])
def createLecture():
    return classes.createLecture()

if __name__ == "__main__":
    app.run() 