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
        count = 0
        errItems = []
        for i in d:
            if addEmployee(i):
                count+=1
            else:
                errItems(i)
        return jsonify({"message":"Data Added Successfully","Total Updated Count":count,"Total Failed Employees":errItems,"Failed Employee Count":len(errItems)})
    return ""

if __name__ == "__main__":
    app.run(debug=True)