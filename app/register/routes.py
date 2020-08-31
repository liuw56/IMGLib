from flask import Blueprint
from flask import redirect, request, render_template, url_for
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user
register = Blueprint('register', __name__)

from ..__init__ import db
from ..database.database import User, login_manager, Inventory, cart
from .services import *

@register.route('/')
def index():
    if current_user.is_authenticated:
        return redirect('/home')
    return render_template('index.html')

@register.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    pw = request.form.get('pw')
    user = User.query.filter_by(email=email).first()
    if not user:
        return "Not Registered"
    login_user(user)
    return redirect('/home')


@register.route('/signup', methods=['POST'])
def signup():
    email = request.form['email']
    name = request.form['name']
    pw = request.form['pw']
    user = addUser(name, email, pw)
    login_user(user)
    return "user added {}".format(user)


@register.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return redirect('/')
