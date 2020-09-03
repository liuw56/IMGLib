from ..__init__ import db
from ..database.database import User, login_manager, Inventory, cart, Item, cart_item
from flask_login import current_user



def checkSession():
    return current_user.is_authenticated

def getCartItem():
    cur_cart = cart.query.filter_by(id=current_user.cart_id).first()
    amt = {'tot': 0}
    for item in cur_cart.items:
        rec = db.engine.execute('select * from cart_item where cart_id={} and item_id={}'.format(cur_cart.id, item.id)).fetchall()[0]
        amt[item.id] = rec[2]
        print(rec)
        amt['tot'] += int(rec[2])* float(item.item_price)
    print(amt)
    return [cur_cart.items, amt]

def deleteItem(id):
    cur_cart = cart.query.filter_by(id=current_user.cart_id).first()
    item = Item.query.filter_by(id=id).first()
    cur_cart.items.remove(item)
    db.session.commit()
    return

def chageItemAmt(id, amt):
    db.engine.execute('Update cart_item set amt={} where cart_id={} and item_id={}'.format(amt, current_user.cart_id, id))
    db.session.commit()
    return

def clearCart():
    cur_cart = cart.query.filter_by(id=current_user.cart_id).first()
    for item in cur_cart.items:
        amt = db.engine.execute('Select amt from cart_item where cart_id={} and item_id={}'.format(current_user.cart_id,item.id)).fetchall()[0][0]
        item.item_num = item.item_num-amt
        if(item.item_num==0):
            db.session.delete(item)
    cur_cart.items = []
    db.session.commit()
    return

def checkStockService():
    cur_cart = cart.query.filter_by(id=current_user.cart_id).first()
    msg = ''
    for item in cur_cart.items:
        amt = db.engine.execute('Select amt from cart_item where cart_id={} and item_id={}'.format(current_user.cart_id,item.id)).fetchall()[0][0]
        if(int(amt) > int(item.item_num)):
            if(msg==''):
                msg = 'Those items are out of stock: '
            cur_cart.items.remove(item)
    db.session.commit()
    return msg
    
