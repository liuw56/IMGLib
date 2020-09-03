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
    email = request.form.get('email').replace(" ", "")
    pw = request.form.get('pw').replace(" ", "")
    user = User.query.filter_by(email=email).first()
    if not user:
        return render_template('index.html', msg = "please sign up first.")
    if user.password != pw:
        return render_template('index.html', msg = "Wrong password")
    login_user(user)
    return redirect('/home')


@register.route('/signup', methods=['POST'])
def signup():
    email = request.form['email']
    name = request.form['name']
    pw = request.form['pw']
    user = addUser(name, email, pw)
    if user:
        return render_template('index.html', msg="The email address has been registered, please log in.")
    login_user(user)
    return redirect('/')


@register.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return redirect('/')
