   timestamp=str(datetime.datetime.date(datetime.datetime.now()))
    name=request.form.get('name')
    dob=request.form.get('age')
    height=request.form.get('height')
    weight=request.form.get('weight')
    age=request.form.get('age')
    sex=request.form.get('gender')
    goal=request.form.get('goal')
    bmi=float(weight/((height/100)*(height/100)))
    if sex==1:
        bmr=(10*weight)+(6.25*height)-(5*age)+5
        if goal=='gain' or goal=='GAIN':
            calintake=bmr*2
        else:
            calintake=1.1*bmr

    if sex==2:
        bmr=(10*weight)+(6.25*height)-(5*age)-161
        if goal=='gain' or goal=='GAIN':
            calintake=1.5*bmr
        else:
            calintake=bmr
    fd=open(username1+'details.txt','a')
    if os.path.getsize(username1+'details.txt')==0:
        fd.write('TIMESTAMP|NAME|DATEOFBIRTH|HEIGHT|WEIGHT|AGE|SEX|BMI|BMR|CALORI INTAKE')
    fd.write('\n'+timestamp+'|'+name+'|'+dob+'|'+ str(height)+'|'+str(weight)+'|'+str(age)+'|'+sex+'|'+ str(bmi)+'|'+str(bmr)+'|'+str(calintake) )
    fd.close()
    return redirect('/login')