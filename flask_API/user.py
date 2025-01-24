from flask import Flask,request,jsonify
import pymysql
import random
from flask_jwt_extended import JWTManager
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
import jwt,json
conn = pymysql.connect(
    host="127.0.0.1",
    user="root",
    passwd="1356",
    database="training"
)
cur = conn.cursor()

app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
jwt_app = JWTManager(app)

@app.route('/addUser',methods=['GET','POST'])
def addUser():
    if request.method == "POST":
        try:
            name = request.form.get('username')
            email = request.form.get('email')
            password = random.randint(100000,999999)
            print(password)
            usertype = request.form.get('type')
            q = f"insert into user(name,email,password,type) values('{name}','{email}','{password}','{usertype}')"
            cur.execute(q)
            conn.commit()
            userData = {"username":name,"email":email,"password":password,"type":usertype}
            encoded_jwt = create_access_token(identity=json.dumps(userData))
            print(encoded_jwt)
            return jsonify({
                "message":"User Created Successfully",
                "userDetails":encoded_jwt
                })
        except Exception as e:
            return jsonify({"Error",e.__str__})
    return ""

@app.route('/getUserData')
@jwt_required()
def getUserData():
    current_user = get_jwt_identity()
    user = json.loads(current_user)
    return jsonify(logged_in_as=user), 200
    
    

if __name__ == "__main__":
    app.run(debug=True)
