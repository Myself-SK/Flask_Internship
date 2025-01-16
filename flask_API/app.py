from flask import Flask, render_template,request

app = Flask(__name__)
import pymysql
conn = pymysql.connect(
    host="127.0.0.1",
    user="root",
    passwd="",
    database="training"
)
cur = conn.cursor()
@app.route('/',methods=["POST","GET"])
def index():
    if request.method == "POST":
        user = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        print(user)
        print(email)
        print(password)
    return render_template('index.html')

@app.route("/user")
def user():
    int_var = 10
    float_var = 3.143
    name = "dhanu"
    lst = [1,2,3,4,5]
    dic = {1:'One',2:'Two'}
    return render_template('values.html',iv= int_var,fv=float_var,sv = name, lv = lst,dv = dic)

@app.route("/users")
def users():
    return "Users page"

@app.route("/<name>")
def greeting(name):
    return f"Hello {name}"

@app.route('/student',methods=["POST","GET"])
def student():
    if request.method == "POST":
        import datetime
        Username = request.form.get('Name')
        Email = request.form.get("Email")
        Password = request.form.get("Password")
        q = f"select * from student where email = '{Email}'"
        cur.execute(q)
        res = cur.fetchall()
        if len(res) > 0:
            return "User Already Exists"
        else:
            q = f"insert into student(name,email,password,created) values('{Username}','{Email}','{Password}','{datetime.datetime.now()}')"
            cur.execute(q)
            conn.commit()
    cur.execute('select * from student')
    res = cur.fetchall()
    return render_template('student.html',students=res)

if __name__ == "__main__":
    app.run(debug=True)