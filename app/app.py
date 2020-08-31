from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import mimetypes
from flask_login import LoginManager, UserMixin
from flask import Flask
from .__init__ import app
# app = Flask(__name__)
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///db.sqlite3"
# app.config['SECRET_KEY'] = '100000'
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)


class Inventory(db.Model):
    id = db.Column(db.Integer, primary_key=True)


cart_item = db.Table(
    'cart_item',
    db.Column('cart_id', db.Integer, db.ForeignKey(
        'cart.id'), primary_key=True),
    db.Column('item_id', db.Integer, db.ForeignKey(
        'item.id'), primary_key=True)
)


class cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    items = db.relationship('Item', secondary=cart_item, lazy='subquery',
                            backref=db.backref('carts', lazy=True))


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    inventory_id = db.Column(db.Integer, db.ForeignKey('inventory.id'))
    item_desc = db.Column(db.String(50))
    item_price = db.Column(db.Integer, nullable=False)
    item_num = db.Column(db.Integer, nullable=False)
    img = db.Column(db.Text)
    mimetype = db.Column(db.Text)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(45), nullable=False)
    inventory_id = db.Column(db.Integer, db.ForeignKey('inventory.id'))
    cart_id = db.Column(db.Integer, db.ForeignKey('cart.id'))
