from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///db.sqlite3"
app.config['SECRET_KEY'] = '100000'
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def get(id):
    from .database.database import User
    user = db.session.query(User).get(id)
    return user

from .database.routes import database
from .register.routes import register
from .home.routes import home
from .checkout.routes import checkout

app.register_blueprint(home)
app.register_blueprint(register)
app.register_blueprint(database)
app.register_blueprint(checkout)