
from ..__init__ import db
from ..database.database import User, login_manager, Inventory, cart

def addUser(name, email, pw):
    check_user = User.query.filter_by(email=email).first()
    if check_user:
        return True
    user = User(name=name, email=email, password=pw)
    inventory = Inventory()
    cart_new = cart()
    db.session.add(inventory)
    db.session.add(cart_new)
    db.session.commit()
    user.cart_id = cart_new.id
    user.inventory_id = inventory.id
    db.session.add(user)
    db.session.commit()
    return user

