from flask import flash,render_template,Flask,request,redirect
import datetime,os
app = Flask(__name__)
app.secret_key='heyy'

@app.route("/")
def Home_Page():
  return render_template("index.html")

@app.route("/login",methods=['GET','POST'])
def login():
    if request.method=="POST":
        with open('login.txt','r') as logRd:
            email=request.form.get('email')
            password=request.form.get('password')
            global username1
            for line in logRd:
                line=line.rstrip('\n')            #remove nextline character
                list=line.split('|')              #convert each record to list to access each element
                if list[0]=='USERNAME':
                    continue
                if list[0]==email or list[1]==email:
                    if list[3]==password:
                        username1=list[0]
                        return redirect('/dashboard')    #get username to pass to dashboard
                    else:
                        flash("incorrect paaword")
                        return redirect('/login')
            if list[0]!=email or list[1]!=email:
                    flash("user does'nt exist.SIGNUP!!")
                    return redirect('/signup')        #retry or go signup
            logRd.close()
    return render_template("login.html")


@app.route("/signup", methods=['GET','POST'])
def signup():
 if request.method=="POST":
    with open('login.txt','a') as logApp:
        with open('login.txt','r') as logRd:
            username=request.form.get('username')
            email=request.form.get('email')
            phoneno=request.form.get('phone')
            password=request.form.get('password')
            global username1
            username1=username
            for line in logRd:
                line=line.rstrip('\n')            #remove nextline character
                list=line.split('|')              #convert each record to list to access each element
            if list[0]=='USERNAME':
                pass
            if list[1]==email or list[2]==phoneno or list[0]==username:
                flash("user already exists.LOGIN!!")
                return render_template("login.html")
        logApp.write('\n'+username+'|'+email+'|'+phoneno+'|'+password )
    return redirect('/user')
 return render_template("signup.html")

@app.route("/user", methods=['GET','POST'])
def userDetails():
#  os.mkdir(r"C:\Users\anish\Desktop\calorie project\customerdetails"+username1)
 if request.method=="POST":
    timestamp=str(datetime.datetime.date(datetime.datetime.now()))
    name=request.form.get('name')
    height=request.form.get('height',type=int)
    weight=request.form.get('weight',type=int)
    age=request.form.get('age',type=int)
    sex=request.form.get('gender')
    goal=request.form.get('goal')
    bmi=(weight/((height/100)*(height/100)))
    bmi=round(bmi,2)
    bmr=0
    if sex=='M':
        bmr=(10*weight)+(6.25*height)-(5*age)+5
        bmr=round(bmr,2)
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
    calintake=round(calintake,2)
    with open(username1+'details.txt','a')as fd:
        if os.path.getsize(username1+'details.txt')==0:
            fd.write('TIMESTAMP|NAME|AGE|HEIGHT|WEIGHT|SEX|GOAL|BMI|BMR|CALORI INTAKE')
        fd.write('\n'+timestamp+'|'+name+'|'+str(age)+'|'+ str(height)+'|'+str(weight)+'|'+sex+'|'+goal+'|'+ str(bmi)+'|'+str(bmr)+'|'+str(calintake) )
    return redirect('/dashboard')
 return render_template("userdetails.html")


@app.route("/dashboard", methods=['GET','POST'])
def dashboard():
    breakfast=[]
    lunch=[]
    dinner=[]
    snacks=[]
    with open(username1+'details.txt','r') as fd:
        for line in fd:
            line=line.rstrip('\n')            #remove nextline character
            list=line.split('|')
            pass
        timestamp=list[0]
        username=username1
        name=list[1]
        age=list[2]
        height=list[3]
        weight=list[4]
        sex=list[5]
        goal=list[6]
        bmi=list[7]
        bmr=list[8]
        calin=list[9]
    if timestamp<str(datetime.datetime.date(datetime.datetime.now())):
        flash("update your details")
    fdem=open(username1+'meal.txt','a')
    fdem.close()   
    heading=[('MEAL','CALORIES/gram')]
    dheadings=[('MEAL','GRAM','CALORIES')]
    items=[]
    items1=[]
    items2=[]
    items3=[]
    with open('meal.txt','r') as fd:
        for line in fd:
            line=line.rstrip('\n')            #remove nextline character
            list=line.split('|')  
            if(list[2]=='B'or list[2]=='A'):
                items.append((list[0],list[1]))   
            if(list[2]=='L'or list[2]=='A'):
                items1.append((list[0],list[1]))
            if(list[2]=='S'):
                items3.append((list[0],list[1]))
            if(list[2]=='D'or list[2]=='A'):
                items2.append((list[0],list[1]))
    
    with open(username1+'meal.txt','r') as fd:
     for line in fd:
         line=line.rstrip('\n')            #remove nextline character
         list=line.split('|')
         if(list[2]=='B'):
             breakfast.append((list[0],list[1],list[3]))   
         if(list[2]=='L'):
             lunch.append((list[0],list[1],list[3]))  
         if(list[2]=='S'):
             snacks.append((list[0],list[1],list[3]))
         if(list[2]=='D' ):
             dinner.append((list[0],list[1],list[3]))
    
    with open(username1+'meal.txt','r') as fd:
        concal=0
        for line in fd:
         line=line.rstrip('\n')            #remove nextline character
         list=line.split('|')
         concal=concal+float(list[3])
         concal=round(concal,2)
         if concal>=float(calin):
            flash("you have consumed more calorie than required")


    return render_template("dashboard.html",username=username,name=name,age=age,height=height,weight=weight,sex=sex,goal=goal,bmi=bmi,bmr=bmr,calin=calin,heading=heading,items=items,items1=items1,items2=items2,items3=items3,breakfast=breakfast,lunch=lunch,snacks=snacks,dinner=dinner,concal=concal,dheadings=dheadings)

@app.route("/addmeal", methods=['GET','POST'])
def addmeal():
    if request.method=="POST":
        fd1=open('meal.txt','r')
        dum=open('dummy.txt','a')
        flag=0
        fd2= open(username1+'meal.txt','r+')
        meal=request.form.get('meal')
        qty=request.form.get('qty',type=int)
        mealtype=request.form.get('mealtype')
        for line in fd1:
            line=line.rstrip('\n')            #remove nextline character
            list=line.split('|')              #convert each record to list to access each element
            if(list[0]==meal):
                flag=1
                concal=float(list[1])*qty
        fd1.close()
        if(flag==0):
            flash("item not in list")
            dum.close()
            os.remove('dummy.txt')
            return redirect('/dashboard')
        for line in fd2:
            line=line.rstrip('\n')            #remove nextline character
            list=line.split('|')              #convert each record to list to access each element
            if(list[0]==meal) and (list[2]==mealtype):
                qty=qty+int(list[1])
                concal=concal+float(list[3])
                concal=round(concal,2)
            else:
                dum.write(line+'\n')
        concal=round(concal,2)
        dum.write(meal+'|'+str(qty)+'|'+mealtype+'|'+str(concal)+'\n')
        dum.close()
        fd2.close()
        os.remove(username1+'meal.txt')
        os.rename('dummy.txt',username1+'meal.txt')

    return redirect('/dashboard')

@app.route("/updatemeal",methods=['GET','POST'])
def updatemeal():
    if request.method=="POST":
        fd1=open('meal.txt','r')
        dum=open('dummy.txt','a')
        flag=0
        fd2= open(username1+'meal.txt','r+')
        meal=request.form.get('meal')
        qty=request.form.get('qty',type=int)
        mealtype=request.form.get('mealtype')
        concal=0
        for line in fd1:
            line=line.rstrip('\n')            #remove nextline character
            list=line.split('|')              #convert each record to list to access each element
            if(list[0]==meal):
                flag=1
                concal=float(list[1])*qty
                fd1.close()
                break
        
        if(flag==0):
            flash("item not in list")
            fd2.close()
            dum.close()
            os.remove('dummy.txt')
            return redirect('/dashboard')
        for line in fd2:
            line=line.rstrip('\n')            #remove nextline character
            list2=line.split('|')              #convert each record to list to access each element
            if(list2[0]==meal) and (list2[2]==mealtype):
                flag=2
                qty=qty
                concal=round(concal,2)
                continue
            else:
                dum.write(line+'\n')
        if flag==2 and qty!=0:
            dum.write(meal+'|'+str(qty)+'|'+mealtype+'|'+str(concal)+'\n')
        dum.close()
        fd2.close()
        os.remove(username1+'meal.txt')
        os.rename('dummy.txt',username1+'meal.txt')
    
    return redirect('/dashboard')


@app.route("/updateform", methods=['GET','POST'])
def update():
    with open(username1+'details.txt','r') as fd:
        for line in fd:
            line=line.rstrip('\n')            #remove nextline character
            list=line.split('|')
            pass
        username=username1
        name=list[1]
        sex=list[5]
        height=int(list[3])
        if request.method=="POST":
            timestamp=str(datetime.datetime.date(datetime.datetime.now()))
            weight=request.form.get('weight',type=int)
            age=request.form.get('age',type=int)
            goal=request.form.get('goal')
            bmi=(weight/((height/100)*(height/100)))
            bmi=round(bmi,2)
            bmr=0
            if sex=='M':
                bmr=(10*weight)+(6.25*height)-(5*age)+5
                if goal=='gain':
                    calintake=bmr*1.7
                else:
                    calintake=1.1*bmr
            if sex=='F':
                bmr=(10*weight)+(6.25*height)-(5*age)-161
                if goal=='gain':
                    calintake=1.5*bmr
                else:
                    calintake=bmr
            calintake=round(calintake,2)
            with open(username1+'details.txt','a')as fd:
                fd.write('\n'+timestamp+'|'+name+'|'+str(age)+'|'+ str(height)+'|'+str(weight)+'|'+sex+'|'+goal+'|'+ str(bmi)+'|'+str(bmr)+'|'+str(calintake) )
            return redirect('/dashboard')
    return render_template("updateform.html",username=username,name=name,sex=sex,height=height)


if __name__ == '__main__':
    app.run(debug=True)