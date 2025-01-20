from flask import Flask,render_template,request
app = Flask(__name__)
@app.route('/',methods=["GET","POST"])
def index():
    if request.method == "POST":
        user = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        print(user)
        print(email)
        print(password)
    return render_template('index.html')

@app.route('/new')
def new():
    int_var = 10
    float_var = 3.143
    name = "dhanu"
    lst = [1,2,3,4,5]
    dic = {1:'One',2:'Two'}
    return render_template('values.html',iv= int_var,fv=float_var,sv = name, lv = lst,dv = dic)


@app.route('/<name>')
def name(name):
    return "Hello {}".format(name)

if __name__ == "__main__":
    app.run(debug=True)