from ..__init__ import db
from ..database.database import User, login_manager, Inventory, cart, Item
from flask_login import current_user

def getInventoryContent():
    inventory_id = current_user.inventory_id
    if not inventory_id:
        return None
    items = Item.query.filter_by(inventory_id=inventory_id).all()
    print(items)
    return items

def getMarketplaceContent():
    items = Item.query.order_by(Item.id).all()
    print(items)
    return items

def addImage(item_desc, img, mimetype, item_price, item_num):
    item = Item(inventory_id=current_user.inventory_id, 
        item_desc=item_desc, 
        item_price=item_price, 
        mimetype=mimetype, 
        img=img,
        item_num=item_num)
    db.session.add(item)
    db.session.commit()
    return
