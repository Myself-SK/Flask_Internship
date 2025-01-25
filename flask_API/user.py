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
cur = conn.cursor(pymysql.cursors.DictCursor)

app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
jwt_app = JWTManager(app)

def checkExist(product_id):
    q = f"select * from product where product_id = '{product_id}'"
    print(q)
    cur.execute(q)
    res = cur.fetchall()
    return len(res) > 0

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
            userData = {"name":name,"email":email,"password":password,"type":usertype}
            encoded_jwt = create_access_token(identity=json.dumps(userData))
            print(encoded_jwt)
            return jsonify({
                "message":"User Created Successfully",
                "userDetails":encoded_jwt
                })
        except Exception as e:
            return jsonify({"Error",e})
    return ""

@app.route('/getUserData')
@jwt_required()
def getUserData():
    current_user = get_jwt_identity()
    user = json.loads(current_user)
    return jsonify(logged_in_as=user), 200
    
@app.route('/addProduct',methods=['POST'])
@jwt_required()
def addProduct():
    
    if request.method == "POST":
        current_user = get_jwt_identity()
        user = json.loads(current_user)
        if user['type'] in ["editor","admin"]:
            try:
                product_id = request.form.get('product_id')
                product_name = request.form.get('product_name')   
                manufacturer = request.form.get('manufacturer')   
                stock = request.form.get('stock')   
                price = request.form.get('price')   
                q = f"insert into product(product_id,product_name,manufacturer,stock,price) values('{product_id}','{product_name}','{manufacturer}','{stock}','{price}')"
                print(q)
                cur.execute(q)
                conn.commit()
                return jsonify({"message":"Product Added Successfully"})
            except Exception as e:
                return jsonify({"Error",e})
        else:
            return jsonify({"message":"You are not authorized to add product"})
    return ""


@app.route('/updateProduct',methods=['POST'])
@jwt_required()
def updateProduct():
    if request.method == "POST":
        current_user = get_jwt_identity()
        user = json.loads(current_user)
        if user['type'] in ["editor","admin"]:
            try:
                product_id = request.form.get('product_id')
                product_name = request.form.get('product_name')   
                manufacturer = request.form.get('manufacturer')   
                stock = request.form.get('stock')   
                price = request.form.get('price')   
                if checkExist(product_id):
                    try:
                        q = f"update product set product_name = '{product_name}',manufacturer = '{manufacturer}',stock = '{stock}',price = '{price}' where product_id = '{product_id}'"
                        print(q)
                        cur.execute(q)
                        conn.commit()
                        return jsonify({"message":"Product Updated Successfully"})
                    except Exception as e:
                        return jsonify({"error":e})    
                else:
                    return jsonify({"message":"product doesn't exist"})
            except Exception as e:
                return jsonify({"Error",e})
    else:
        return jsonify({"message":"You are not authorized to update product"})
    return ""

@app.route('/deleteProduct',methods=['POST'])
@jwt_required()
def deleteProduct():
    if request.method == "POST":
        current_user = get_jwt_identity()
        user = json.loads(current_user)
        if user['type'] in ["admin"]:

            try:
                product_id = request.form.get('product_id')
                print(product_id)
                if checkExist(product_id):
                    try:
                        q = f"delete from product where product_id = '{product_id}'"
                        cur.execute(q)
                        conn.commit()
                        return jsonify({"message":"Product Deleted Successfully"})
                    except Exception as e:
                        return jsonify({"error":e})    
                else:
                    return jsonify({"message":"product doesn't exist"})
            except Exception as e:
                return jsonify({"Error",e})
        else:
            return jsonify({"message":"You are not authorized to delete product"})
    return ""

@app.route('/readProducts')
@jwt_required()
def read():
    q = "select * from product"
    cur.execute(q)
    res = cur.fetchall()
    import pandas as pd
    data = pd.DataFrame(res)
    return data.to_dict('records')

if __name__ == "__main__":
    app.run(debug=True)
