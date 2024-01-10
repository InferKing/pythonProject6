from flask import Flask
from config import *
from flask_mail import Mail
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SECRET_KEY"] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:12345@localhost/todo'
app.config["MAIL_SERVER"] = 'smtp.yandex.ru'
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = FLASK_MAIL
app.config["MAIL_DEFAULT_SENDER"] = FLASK_MAIL
app.config["MAIL_PASSWORD"] = FLASK_PSW
db = SQLAlchemy(app)
mail = Mail(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

if __name__ == '__main__':
    from views import *
    app.run(debug=True)
