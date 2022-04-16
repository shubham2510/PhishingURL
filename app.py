import numpy as np
import pandas as pd
from flask import Flask, flash, request, render_template, flash, redirect, url_for, session,  request, abort
from sklearn import metrics 
import warnings
warnings.filterwarnings('ignore')
from feature import generate_data_set
# Gradient Boosting Classifier Model
from sklearn.ensemble import GradientBoostingClassifier

data = pd.read_csv("phishing.csv")
#droping index column
data = data.drop(['Index'],axis = 1)
# Splitting the dataset into dependant and independant fetature

X = data.drop(["class"],axis =1)
y = data["class"]

# instantiate the model
gbc = GradientBoostingClassifier(max_depth=4,learning_rate=0.7)

# fit the model 
gbc.fit(X,y)
import config
from datetime import datetime

import mysql.connector


import pickle




mydb = mysql.connector.connect(
 host="remotemysql.com",
  user="MKnq4tnVGc",
  password="GmiR1Xo6G2",
  database="MKnq4tnVGc"
)

mycursor = mydb.cursor(buffered=True)

app = Flask(__name__)
model = pickle.load(open('model.pkl', 'rb'))

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'



@app.route('/')
def home():
    return render_template('home.html',login=config.isLoggedIn())   

@app.route('/home')
def hom():
    return render_template('home.html',login=config.isLoggedIn())




@app.route('/signup')
def signup():
    return render_template('register.html',login=config.isLoggedIn())

@app.route('/signup', methods=['GET', 'POST'])
def register_post():
    # Output message if something goes wrong...
    msg = '' 
    
    name = request.form['name']
    
    mobile = request.form['mob'] 
    email = request.form['email'] 
    password = request.form['password']
    
    mycursor.execute('SELECT * FROM users WHERE email =%s',(email,))
    account = mycursor.fetchone() 
    if account: 
        msg = 'Account already exists !'
    else:
        sq='INSERT INTO users VALUES (NULL, %s, %s, %s, %s)'
        mycursor.execute(sq, (name, mobile, email,  password, )) 
        mydb.commit()
        msg = 'You have successfully registered !'    
    return render_template('register.html', msg = msg) 


@app.route('/login')
def login():
    return render_template('log.html',login=config.isLoggedIn())

@app.route('/login', methods =['POST']) 
def login_post(): 
    msg = ''
    email = request.form['txtEmail']  
    password = request.form['password'] 
    print(email)
    print(password)
   
    mycursor = mydb.cursor(buffered=True)
    mycursor.execute('SELECT * FROM users WHERE email = %s and password = %s', (email, password, )) 
    account = mycursor.fetchone()  
    if account: 
        session['loggedin'] = True
        session['id'] = account[0] 
        session['name'] = account[1] 
        session['email'] = account[3]
        session['mobile'] = account[4] 
        msg = 'Logged in successfully !'
        return redirect(url_for('dashboard')) 
    else: 
        msg = 'Incorrect username / password !'
        return render_template('log.html', msg = msg) 

@app.route('/contact')
def contactus():
    return render_template('contact-us.html',login=config.isLoggedIn())

@app.route('/contact', methods=['POST'])
def contact_form_post():
    mycursor = mydb.cursor()
    name = request.form['name']
    mobile = request.form['phonenumber']
    email = request.form['email']
    messageData = request.form['messages']


    try:
        sq='INSERT INTO contact VALUES (%s, %s, %s, %s, NULL)'
        mycursor.execute(sq, (name, mobile, email, messageData, )) 
        mydb.commit()
        flash="Hey "+ name +"! Your Message Has Been Sent Successfully ."
    except:
        flash="Hey "+ name +"! Sorry ... Some Internal Problem"
    return render_template('contact-us.html', flash=flash) 

@app.route('/dashboard')
def dashboard():
    if config.isLoggedIn():
        return redirect(url_for('profile'))
    else:
        return redirect(url_for('login'))


@app.route('/dashboard/profile')
def profile():
    if config.isLoggedIn():
        uid=session['id']

        mycursor.execute('SELECT * FROM users WHERE uid =%s',(uid,))
        
        account = mycursor.fetchone()
        
        if account:
            name = account[1] 
            mobile = account[2]
            
            mycursor.execute('SELECT * FROM predict WHERE uid =%s',(uid,))
            acc = mycursor.fetchone()
            glucose=0
            url=acc[2]
            typeof=''
            if acc is not None: 
                if acc[3] == '1.0':
                    predict=True
                    
                else:
                    predict=False
            else:
                predict=False







        return render_template('dashboard/profile.html',login=config.isLoggedIn(),uid=session['id'], name=name,mobile=mobile,predict=predict,glucose=glucose,url=url)
    else:
        return redirect(url_for('login'))
    
  
@app.route('/dashboard/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('email', None)
    session.pop('id', None)
    session.pop('name', None)
  
    flash="Logged Out Successfully"
    
    return render_template('log.html',msg1=flash)

@app.route('/dashboard/logout',methods=['POST'])
def logout_post():
    msg = ''
    email = request.form['txtEmail']  
    password = request.form['password'] 
    print(email)
    print(password)
   
    mycursor = mydb.cursor(buffered=True)
    mycursor.execute('SELECT * FROM users WHERE email = %s and password = %s', (email, password, )) 
    account = mycursor.fetchone()  
    if account: 
        session['loggedin'] = True
        session['id'] = account[0] 
        session['name'] = account[1] 
        session['email'] = account[3]
        session['mobile'] = account[4] 
        msg = 'Logged in successfully !'
        return redirect(url_for('dashboard')) 
    else: 
        msg = 'Incorrect username / password !'
        return render_template('log.html', msg = msg) 


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html',login=config.isLoggedIn())

@app.route('/predict')
def prdict():
    if config.isLoggedIn():
        return render_template('index.html',login=config.isLoggedIn())
    else:
        return redirect(url_for('login'))

@app.route('/predict',methods=["GET", "POST"])
def predict():
    if request.method == "POST":
        uid=session['id']

        url = request.form["url"]
        x = np.array(generate_data_set(url)).reshape(1,30) 
        y_pred =gbc.predict(x)[0]
        #1 is safe       
        #-1 is unsafe
        y_pro_phishing = gbc.predict_proba(x)[0,0]
        y_pro_non_phishing = gbc.predict_proba(x)[0,1]
        # if(y_pred ==1 ):
        pred = "It is {0:.2f} % safe to go ".format(y_pro_phishing*100)
        predict=round(y_pro_non_phishing,2)       
        mycursor.execute('SELECT * FROM predict WHERE uid = %s ', (uid, )) 
        account = mycursor.fetchone()  
        if account:
            sql='UPDATE `predict` SET `predict`=%s,`url`=%s WHERE uid =%s'
            mycursor.execute(sql, (predict,url,uid, ))
            mydb.commit()
        else:
            sql='INSERT INTO predict VALUES (NULL, %s, %s, %s)'
            mycursor.execute(sql, (uid,  url, predict,))
            mydb.commit()
        return render_template('index.html',xx =round(y_pro_non_phishing,2),url=url )
        # else:
        #     pred = "It is {0:.2f} % unsafe to go ".format(y_pro_non_phishing*100)
        #     return render_template('index.html',x =y_pro_non_phishing,url=url )
        
    return render_template("index.html", xx =-1)


if __name__ == "__main__":
    app.run(debug=True)
