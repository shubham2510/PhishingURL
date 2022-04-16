
from flask import session,flash
from datetime import datetime
config = {
    "apiKey": "#########################################",
    "authDomain": "#########################",
    "databaseURL": "#################################",
    "projectId": "############",
    "storageBucket": "######################",
    "messagingSenderId": "############"
}



def register_with_email_and_password(name,phone,email,password):
    try:
        user=auth.create_user_with_email_and_password(email,password)
        auth.send_email_verification(user['idToken'])
        Register(name,email,phone)
        return True
    except:
        return False

def signin_with_email_and_password(email,password):
    try:
        user=auth.sign_in_with_email_and_password(email,password)
        session['username'] = user['email']
        session['id'] = user['localId']
        jsonv = profiledata().val()
        for key in jsonv:
            session['name']=jsonv[key]['name']
            session['phone']=jsonv[key]['phone']
        return True
    except:
        return False

def reset_password_with_email(email):
    try:
        auth.send_password_reset_email(email)
        return True
    except:
        return False

def sendMessage(name,phoneNum,email,message):
    data = {
    "name": name ,
    "email": email ,
    "phone": phoneNum ,
    "message": message
    }
    db.child("messages").push(data)

def Register(name,email,phoneNum):
    data = {
    "name": name ,
    "email": email ,
    "phone": phoneNum ,
    }
    db.child("users").child(session['id']).push(data)

def historify(id,query,ip):
    data = {
    "query": query ,
    "time": str(datetime.now()) ,
    "ip": str(ip) ,
    }
    db.child("history").child(id).push(data)

def isLoggedIn():
    if 'email' in session:
        return True
    else:
        return False

def profiledata():
    return db.child("users").child(session['id']).get()

def history():
    try:
        return db.child("history").child(session['id']).get()
    except:
        return False
