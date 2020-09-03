from flask import Blueprint, render_template,redirect, request, url_for
from flask_login import current_user
import mimetypes
import base64

home = Blueprint('home', __name__, url_prefix='/home')

from .services import *

@home.route('/')
def index():
    if not checkSession():
        return redirect('/')
    items = getMarketplaceContent()
    return render_template('home.html', name=current_user.name, items=items)

@home.route('/myitems')
def myimages():
    if not checkSession():
        return redirect('/')
    items = getInventoryContent()
    return render_template('myitems.html', items=items, user=current_user)

@home.route('/upload', methods=['GET','POST'])
def upload():
    if not checkSession():
        return redirect('/')
    if request.method=='GET':
        return render_template('upload.html', name=current_user.name)
    if request.method == 'POST':
        pic = request.files.get('pic')
        if not pic:
            return render_template('upload.html', name=current_user.name, message="Please upload a image")
        if(not pic.filename.lower().endswith(('.png', '.jpg', '.jpeg'))):
            return "Please select files with .png, .jpg or .jpeg extensions"
        pic_base64 = base64.b64encode(pic.read()).decode('utf-8')
        item_price = request.form.get('item_price').strip()
        item_num = request.form.get('item_num').strip()
        valid = checkNumType(item_price, item_num)
        if not valid==True:
            return render_template('upload.html', name=current_user.name, message=valid)
        addItem(request.form.get('item_desc'), 
            pic_base64, 
            pic.mimetype, 
            item_price,
            item_num,
            request.form.get('item_name')
            )
        return redirect('/home/myitems')

@home.route('/iteminfo/<int:id>')
def iteminfo(id):
    if not checkSession():
        return redirect('/')
    item = Item.query.filter_by(id=id).first()
    if not item:
        return "Item Not Found"
    return render_template('iteminfo.html', item=item)

@home.route('myitems/delete/<int:id>')
def delete(id):
    if not checkSession():
        return redirect('/')
    item = deleteItem(id)
    if not item:
        return "Item is not found"
    return redirect('/home/myitems')

@home.route('myitems/update/<int:id>', methods=['POST', 'GET'])
def update(id):
    if not checkSession():
        return redirect('/')
    item = Item.query.filter_by(id=id).first()
    if not item:
        return "Item not found"
    if request.method =='GET':
        return render_template("update.html", name=current_user.name, item=item)
    if request.method == 'POST':
        pic = request.files.get('pic')
        pic_base64 = None
        mimetype = None
        if pic.filename!='':
            if(not pic.filename.lower().endswith(('.png', '.jpg', '.jpeg'))):
                return "Please select files with .png, .jpg or .jpeg extensions"
            pic_base64 = base64.b64encode(pic.read()).decode('utf-8')
            mimetype = pic.mimetype
        item_price = request.form.get('item_price').strip()
        item_num = request.form.get('item_num').strip()
        valid = checkNumType(item_price, item_num)
        if not valid==True:
            return render_template('upload.html', name=current_user.name, message=valid, item=item)
        updateItem(item,
            request.form.get('item_desc'), 
            pic_base64, 
            pic.mimetype, 
            item_price,
            item_num,
            request.form.get('item_name')
        )
        return redirect('/home/myitems')

@home.route('/addtocart/<int:id>')
def addToCart(id):
    add(id)
    return redirect('/home')