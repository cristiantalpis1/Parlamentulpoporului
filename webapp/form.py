from webapp.database import inregistrare , verificare , verificare_pass , inregistrare_changes_db
from argon2 import PasswordHasher
from flask_mail import Message
from webapp import otp, otp_phone, mail, app
from twilio.rest import Client 
from flask import session
from random import randint

def password_hash(pass1):
    ph = PasswordHasher()
    hash = ph.hash(pass1)
    return hash


def verify_register_form(user, email, phone, password, conf_pass):
    e=""
    passwordh = None
    taken_username = False 
    taken_email = False
    taken_phone = False

    a=verificare("username",user)
    if a: 
        e=e+" Acest nume de utilizator este folosit! "
        taken_username = True

    a=verificare("email", email)
    if a:
        e=e+" Acest email este deja folosit! "
        taken_email = True

    phone_nr = phone_restructure(str(phone))
    a=verificare("phone", phone_nr)
    if a:
        e=e+" Acest numar de telfon este deja folosit! "
        taken_phone = True
    
    if password!=conf_pass :
        e=e+" Parola Gresita "
    if e=="":
        passwordh=password_hash(password)
        e="Inregistrare completa"
        
    return e, taken_username, taken_email, taken_phone,passwordh, phone_nr

def phone_restructure(phone_nr):
    if phone_nr[0] == '+':
        nr_restr = phone_nr
    elif phone_nr[0] == '0':
        nr_restr = '+373' + phone_nr[1:]
    else:
        nr_restr = '+373' + phone_nr
    print(nr_restr)
    return nr_restr
    

def autentificarea(email, user, password):
    e=""
    a=verificare("username",user)
    if not(a):
        e=e+"Acest username sau email este invalid"
    else :
        a=verificare_pass(password, email)
        if a==True:
            e=""
        else:
            e="Parola gresita" 
    return e

def reset_pass(password_old,password,conf_password,email):
    a=verificare_pass(password_old, email)
    e=""
    if a==True:
        if password==conf_password :
            pas=password_hash(password)
            inregistrare_changes_db('password', pas, email)
        else:
            e="Parloa de confirmare gresita"
    else :
        e="parola gresita"
    return e

def user_in_db(user):
    error = ''
    a = verificare("username", user)
    if not(a):
        error = "Aceasta pagina este invalida"
    else:
        error = ''
    return error

def send_otp(email):
    msg = Message(subject='OTP', sender='parlamentulpoporului@gmail.com', recipients=[email])
    msg.body = str(otp)
    mail.send(msg)
    return str(otp)

def send_otp_phone(phone_nr):
    account_sid = 'ACfd8f42b2319e166669e54f00026c5def' 
    auth_token = '45f6a03597ba738beeb6fe0557f774c4' 
    client = Client(account_sid, auth_token) 
    message = client.messages.create(  
                                messaging_service_sid='MGa91850e937131d1178348517855ca354', 
                                body=otp_phone,      
                                to=phone_nr
                            ) 
    return str(otp_phone)

def register_user(username, email, phone, passwordhs): 
    error = ''
    try:
        inregistrare(username, email, phone, passwordhs)
    except:
        error = 'error'
    return error

def verify_changes(username, username_form, email, email_form):
    error1 = ''
    error2 = ''
    gl_username = username
    gl_email = email
    
    if username_form == username:
        pass
    else:
        var = verificare("username", username_form)
        if var:
            error1 = "Acest username este deja luat!"
        else:
            inregistrare_changes_db('username', username_form, email)
            session["username"]=username_form
            gl_username = username_form

    if email_form == email:
        pass
    else:
        var = verificare("email", email_form)
        if var:
            error2 = "Acest email este deja luat!"
        else:
            
            inregistrare_changes_db('email', email_form, email)
            session["email"]=email_form
            gl_email = email_form
    return gl_username, gl_email, error1, error2

def create_otp():
    otp1 = randint(100000, 999999)
    return otp1
    
        