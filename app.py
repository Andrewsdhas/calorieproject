from flask import *
import datetime,os
app = Flask(__name__)

@app.route("/")
def Home_Page():
  return render_template("index.html")

@app.route("/login",methods=['GET','POST'])
def login():
    if request.method=="POST":
        logRd=open('login.txt','r')
        email=request.form.get('email')
        password=request.form.get('password')
        for line in logRd:
            line=line.rstrip('\n')            #remove nextline character
            list=line.split('|')              #convert each record to list to access each element
            if list[0]=='Name' or list[1]==email:
                if list[3]==password:
                    print('login success')    #get username to pass to dashboard
                    exit(0)
                else:
                    print('incorrect password')

        print('record does not exist')         #retry or go signup
        logRd.close()
        return redirect('/dashboard')
    return render_template("login.html")


@app.route("/signup", methods=['GET','POST'])
def signup():
 if request.method=="POST":
    logApp=open('login.txt','a')
    logRd=open('login.txt','r')
    username=request.form.get('username')
    email=request.form.get('email')
    phoneno=request.form.get('phone')
    password=request.form.get('password')
    global username1
    username1=username
    for line in logRd:
        line=line.rstrip('\n')            #remove nextline character
        list=line.split('|')              #convert each record to list to access each element
        if list[0]=='Name':
            continue
        # if list[1]==email or list[2]==phoneno or list[0]==username:
        #     return render_template("signup.html")
    logApp.write('\n'+username+'|'+email+'|'+phoneno+'|'+password )
    logApp.close()
    logRd.close()
    return redirect('/user')
 return render_template("signup.html")

@app.route("/user", methods=['GET','POST'])
def userDetails():
 if request.method=="POST":
    timestamp=str(datetime.datetime.date(datetime.datetime.now()))
    name=request.form.get('name')
    dob=request.form.get('age')
    height=int(request.form.get('height'))
    weight=request.form.get('weight',type=int)
    age=request.form.get('age',type=int)
    sex=request.form.get('gender')
    goal=request.form.get('goal')
    bmi=(weight/((height/100)*(height/100)))
    bmr=0
    if sex=='M':
        bmr=(10*weight)+(6.25*height)-(5*age)+5
        if goal=='gain':
            calintake=bmr*2
        else:
            calintake=1.1*bmr

    if sex=='F':
        bmr=(10*weight)+(6.25*height)-(5*age)-161
        if goal=='gain':
            calintake=1.5*bmr
        else:
            calintake=bmr
    fd=open(username1+'details.txt','a')
    if os.path.getsize(username1+'details.txt')==0:
        fd.write('TIMESTAMP|NAME|DATEOFBIRTH|HEIGHT|WEIGHT|AGE|SEX|BMI|BMR|CALORI INTAKE')
    fd.write('\n'+timestamp+'|'+name+'|'+dob+'|'+ str(height)+'|'+str(weight)+'|'+str(age)+'|'+sex+'|'+ str(bmi)+'|'+str(bmr)+'|'+str(calintake) )
    fd.close()
    return redirect('/dashboard')
 return render_template("userdetails.html")


@app.route("/dashboard", methods=['GET','POST'])
def dashboard():
  return render_template("dashboard.html")



if __name__ == '__main__':
     app.run(debug=True)