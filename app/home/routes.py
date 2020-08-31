from flask import Blueprint, render_template,redirect, request, url_for
from flask_login import current_user
import mimetypes

home = Blueprint('home', __name__, url_prefix='/home')

from .services import *

@home.route('/')
def index():
    if not current_user.is_authenticated:
        return redirect('/')
    return render_template('home.html', name=current_user.name)

@home.route('/myitems')
def myimages():
    items = getInventoryContent()
    return render_template('home.html', items=items)

@home.route('/marketplace')
def marketplace():
    items = getMarketplaceContent()
    return render_template('home.html', items=items)

@home.route('/upload', methods=['GET','POST'])
def upload():
    if request.method=='GET':
        return render_template('upload.html')
    if request.method == 'POST':
        pic = request.files.get('pic')
        mimetype = pic.mimetype
        addImage(request.form.get('item_desc'), 
            pic.read(), 
            mimetype, 
            request.form.get('item_price'),
            request.form.get('item_num'))
        return "image added"
    