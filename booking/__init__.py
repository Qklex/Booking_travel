from flask import Flask
from flask_admin import Admin
from flask_login import LoginManager
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'somepassword'
app.config['FLASK_ADMIN_SWATCH'] = 'Simplex'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shows.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAIL_SERVER'] = 'smtp.yandex.ru'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'email'
app.config['MAIL_DEFAULT_SENDER'] = 'email'
app.config['MAIL_PASSWORD'] = 'password'
app.config['MAIL_USE_TLS'] = False
app.config["MAIL_USE_SSL"]=True
db = SQLAlchemy(app)
admin = Admin(app, name='Booking', template_mode='bootstrap4')
mail = Mail(app)
manager = LoginManager(app)

from booking import models, routes

with app.app_context():
    db.create_all()
