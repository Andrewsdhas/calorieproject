logRd=open('login.txt','r')
email=input('enter email:')
password=input('enter password:')
for line in logRd:
    line=line.rstrip('\n')            #remove nextline character
    list=line.split('|')              #convert each record to list to access each element
    if list[0]=='Name' or list[1]==email:
        if list[3]==password:
            print('login success')    #get username to pass to dashboard
            exit(0)
        else:
            print('incorrect password')

print('record doesnot exist')         #retry or go signup
logRd.close()