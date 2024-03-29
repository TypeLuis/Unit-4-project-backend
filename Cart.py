from crypt import methods
from flask import Blueprint, render_template, session, abort, request

import os
import jwt
import json
import models
import base64
from datetime import datetime

cart = Blueprint("cart", __name__)



@cart.route('/order', methods=["GET"])
def order_route():
    decrypted_id = jwt.decode(
        request.headers["Authorization"],
        os.environ.get("JWT_SECRET"),
        algorithms="HS256",
    )["user_id"]


    user = models.User.query.filter_by(id=decrypted_id).first()

    cart_list = []
    for cart in user.carts:
        cart_list.append(cart.to_json())
    
    return {"carts": cart_list}



@cart.route("/cart", methods=["POST", "GET", "PUT", "DELETE"])
def cart_routes():

    decrypted_id = jwt.decode(
        request.headers["Authorization"],
        os.environ.get("JWT_SECRET"),
        algorithms="HS256",
    )["user_id"]


    user = models.User.query.filter_by(id=decrypted_id).first()

    if request.method == "GET":
        cart_list = []
        dictt = {}
        for cart in user.carts:
            if cart.checkedOut == False:
                
                if cart.item_name in dictt:
                    dictt[cart.item_name]['quantity'] += 1
                
                elif cart.item_name not in dictt:
                    dictt[cart.item_name] = {
                        'quantity' : 1,
                        'price' : int(float(cart.item_price) * 100),
                        "info" : cart.to_json()
                    }

        for key in dictt:
            cart_list.append(dictt[key])
        return {"carts": cart_list}

    elif request.method == "POST":
        cart = models.Cart(
            item_name=request.json["item_name"],
            item_price=request.json["item_price"],
            item_link=request.json["item_link"],
            item_img=request.json["item_img"],
            checkout_date=None,
            checkedOut=False,
        )

        user.carts.append(cart)

        models.db.session.add(user)
        models.db.session.add(cart)

        models.db.session.commit()

        return {"Success": "Item added to cart"}

    elif request.method == "PUT":
        carts = models.Cart.query.filter_by(
            userId=decrypted_id, checkout_date=None
        ).all()

        for cart in carts:
            cart.checkout_date = request.json["date"]
            cart.checkedOut = True
            models.db.session.add(cart)

        models.db.session.commit()

        return {
            "carts": [c.to_json() for c in carts],
            "success": "Items checked out successfully",
        }

    # http://localhost:5001/cart?id=1
    elif request.method == "DELETE":
        cartId = int(request.args.get("id"))
        cart = models.Cart.query.filter_by(
            id=cartId, userId=decrypted_id, checkedOut="false"
        ).first()

        print(cart)

        models.db.session.delete(cart)

        models.db.session.commit()

        return {"Success": "Item removed from cart"}
