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