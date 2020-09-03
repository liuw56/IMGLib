from ..__init__ import db
from ..database.database import User, login_manager, Inventory, cart, Item, cart_item
from flask_login import current_user

def getInventoryContent():
    inventory_id = current_user.inventory_id
    if not inventory_id:
        return None
    items = Item.query.filter_by(inventory_id=inventory_id).all()
    return items

def getMarketplaceContent():
    items = Item.query.order_by(Item.id).all()
    return items

def checkNumType(item_price, item_num):
    if (isNumber(item_price) & item_num.isnumeric()):
        item_num = float(item_num)
        item_price=float(item_price)
        if(float(item_num)%1 != 0):
            return "please enter a integer number of items"
        if(item_num <=0):
            return "item number must be greater than 0"
        if(item_price<0):
            return "item price must be greater or equal to 0"
        return True
    else:
        print(item_price.isnumeric(), item_num.isnumeric())
        return "Please check item number and item price"

def isNumber(item_price):
    try: 
        float(item_price)
        return True
    except ValueError:
        return False

def checkSession():
    return current_user.is_authenticated

def addItem(item_desc, img, mimetype, item_price, item_num, item_name):
    item = Item(inventory_id=current_user.inventory_id, 
        item_desc=item_desc, 
        item_price=item_price, 
        mimetype=mimetype, 
        img=img,
        item_num=item_num,
        item_name=item_name)
    db.session.add(item)
    db.session.commit()
    return

def deleteItem(id):
    item = Item.query.filter_by(id=id).first()
    if not item:
        return False
    db.session.delete(item)
    db.session.commit()
    return True

def updateItem(item, item_desc, img, mimetype, item_price, item_num, item_name):
    if not img==None:
        item.img = img
        item.mimetype = mimetype
    item.item_desc = item_desc
    item.item_name = item_name
    item.item_num = item_num
    item.item_price = item_price
    db.session.commit()
    return

def add(id):
    cur_cart = cart.query.filter_by(id=current_user.cart_id).first()
    item = Item.query.filter_by(id=id).first()
    if not cart or not item:
        return False
    exist_rec = db.engine.execute('select * from cart_item where cart_id={} and item_id={}'.format(cur_cart.id, item.id)).fetchall()
    if exist_rec==[]:
        cur_cart.items.append(item)
        db.session.commit()
        stat = 'update cart_item set amt={} where cart_id={} and item_id={}'.format(1, cur_cart.id, item.id)
        db.engine.execute(stat)
    else:
        exist_rec = exist_rec[0]
        amt = int(exist_rec[2])
        db.engine.execute('update cart_item set amt={} where cart_id={} and item_id={}'.format(amt+1, cur_cart.id, item.id))
        db.session.commit()
    return