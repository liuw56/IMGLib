from flask import Blueprint, render_template,redirect, request, url_for
from flask_login import current_user

checkout = Blueprint('checkout', __name__, url_prefix="/checkout")

from .services import *
@checkout.route('/cart')
def cart():
    if not checkSession():
        return redirect('/')
    res = getCartItem()
    items = res[0]
    amt = res[1]
    return render_template("cart.html", name=current_user.name,
        items=items, amt=amt)

@checkout.route('/delete/<int:id>')
def delete(id):
    if not checkSession():
        return redirect('/')
    deleteItem(id)
    return redirect("/checkout/cart")

@checkout.route('/changeamt/<int:id>/<int:amt>')
def changeAmt(id, amt):
    if not isinstance(amt, int) or int(amt)<0 or amt=='':
        print("not doing anything")
        redirect ('/checkout/cart')
    if amt==0:
        print("amt is 0")
        return redirect('/checkout/delete/{}'.format(id))
    chageItemAmt(id, amt)
    return redirect('/checkout/cart')