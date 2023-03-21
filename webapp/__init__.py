from flask import Flask
from random import *
from flask_mail import Mail
app = Flask(__name__)

app.config['SECRET_KEY'] = '969bde9448eb7e83012c9d5d8d0f0ada'

app.config["MAIL_SERVER"] = 'smtp.gmail.com'
app.config["MAIL_PORT"] = 465
app.config["MAIL_USERNAME"] = 'parlamentulpoporului@gmail.com'
app.config["MAIL_PASSWORD"] = 'sthhvyzwvrjtbdwb'
app.config["MAIL_USE_TLS"] = False
app.config["MAIL_USE_SSL"] = True
mail = Mail(app)
otp = randint(100000, 999999)
otp_phone = randint(1000,9999)

