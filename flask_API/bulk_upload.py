from flask import Flask,request,jsonify
import pandas as pd
import pymysql
conn = pymysql.connect(
    host="127.0.0.1",
    user="root",
    passwd="1356",
    database="training"
)
cur = conn.cursor()
app = Flask(__name__)

def addEmployee(data):
    try:
        q = f"insert into employee(empId,name,designation,email) values('{data['empId']}','{data['name']}','{data['designation']}','{data['email']}')"
        cur.execute(q)
        conn.commit()
        return True
    except:
        return False

def updateEmployee(data):
    try:
        q = f"update employee set name='{data['name']}', designation='{data['designation']}' where email='{data['email']}' and empId = '{data['empId']}'"
        cur.execute(q)
        conn.commit()
        return True
    except:
        return False

def deleteEmployee(data):
    try:
        q = f"delete from employee where email='{data['email']}' and empId = '{data['empId']}'"
        cur.execute(q)
        conn.commit()
        return True
    except:
        return False

def checkExist(data):
    try:
        q = f"select * from employee where email = '{data['email']}'"
        cur.execute(q)
        res = cur.fetchall()
        if len(res)>0:
            return True
        else:
            return False
    except:
        pass

def driverCode(data):
    try:

        if data['Action'] == "Add":
            if checkExist(data):
                updateEmployee(data)
            else:
                addEmployee(data)

        if data['Action'] == "Update":
            if not checkExist(data):
                return False
            else:
                updateEmployee(data)
        if data['Action'] == "Delete":
            if checkExist(data):
                deleteEmployee(data)
            else:
                return False
    except:
        pass
 
@app.route("/",methods=["GET","POST"])
def index():
    if request.method == "POST":
        print(request.files)
        f = request.files.get("employee Details")
        f.save(f.filename)
        print(f.filename)
        data = pd.read_excel(f.filename)
        print(data.head())
        d = data.to_dict("records")
        updatedCount = 0
        addedCount = 0
        failedCount = 0
        errItems = []
        for i in d:
            driverCode(i)
        return jsonify({
            "message":"Data Added Successfully",
            # "Total Added Count":addedCount,
            # "Total Updated Count":updatedCount,
            # "Total Failed Count":failedCount,
            # "Total Failed Employees":errItems,
            # "Failed Employee Count":len(errItems)
            })
    return ""

if __name__ == "__main__":
    app.run(debug=True)


# delete from <table> where <col>=<value>z