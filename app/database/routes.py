from flask import Flask
import mimetypes
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from flask import Blueprint

database = Blueprint('databse', __name__)




@database.route('/data')
def data():
    return "dtatabase"