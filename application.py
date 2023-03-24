
# Importing modules
import models
import jwt
from flask_bcrypt import Bcrypt
from Cart import cart
from newEgg import new_egg
from ebay import ebay
import os
from flask import Flask, request, redirect
from flask_cors import CORS
import sqlalchemy
from bs4 import BeautifulSoup as bs
import requests
import re
import json
import stripe
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv

load_dotenv()


stripe.api_key = os.environ.get('Stripe_Test_Key')  # Stripe test api key


app = Flask(__name__)
CORS(app)


bcrypt = Bcrypt(app)

uri = uri = os.getenv("DATABASE_URL") 
if uri and uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)
#     uri = uri.replace("postgres://", "postgresql+psycopg2://", 1)
# print(uri)

app.config["SQLALCHEMY_DATABASE_URI"] = uri

migrate = Migrate(app, models.db)
models.db.init_app(app=app)


app.register_blueprint(ebay)

app.register_blueprint(new_egg)

app.register_blueprint(cart)


@app.route('/', methods=['GET'])
def root():
    return {"message": 'ok'}


# Backend code for stripe checkout
@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    try:

        # decrypts user's Id
        decrypted_id = jwt.decode(
            request.json["id"],
            os.environ.get("JWT_SECRET"),
            algorithms="HS256",
        )["user_id"]

        # Gets user by ID
        user = models.User.query.filter_by(id=decrypted_id).first()
        # user = models.User.query.filter_by(id=decrypted_id).first()

        cart_list = []
        dictt = {}
        # Gets data from user's cart and formats it in data stripes understands
        for cart in user.carts:
            if cart.checkedOut == False:

                if cart.item_name in dictt:
                    dictt[cart.item_name]['quantity'] += 1

                elif cart.item_name not in dictt:
                    dictt[cart.item_name] = {
                        'price_data': {
                            'currency': 'usd',
                            'product_data': {
                                'name': cart.item_name,
                            },
                            # payment amount has to be given by penny amount
                            'unit_amount': int(float(cart.item_price) * 100),
                        },
                        'quantity': 1,
                    }

        for key in dictt:
            cart_list.append(dictt[key])

        print(cart_list)

        session = stripe.checkout.Session.create(
            shipping_address_collection={
                'allowed_countries': ['US', 'CA'],
            },
            line_items=cart_list,
            mode='payment',
            success_url=f'https://store-search-project.herokuapp.com/order/checkout?success=true',
            cancel_url=f'https://store-search-project.herokuapp.com/order/checkout?canceled=true',
        )

        print(session)
        # return redirect(session.url, code=303)
        return {'url': session.url}

    except Exception as e:
        return str(e)


@app.route("/users", methods=["POST"])
def create_user():
    hashed_pw = bcrypt.generate_password_hash(
        request.json["password"]).decode("utf-8")
    print(models.User)
    try:
        print(request.get_json()['email'])
        user = models.User(email=request.json["email"], password=hashed_pw,)
        print(json.dumps(user.to_json()))

        models.db.session.add(user)
        models.db.session.commit()

        print(user.to_json())
        encrypted_id = jwt.encode(
            {"user_id": user.id}, os.environ.get("JWT_SECRET"), algorithm="HS256"
        )

        return {"user": user.to_json(), "user_id": encrypted_id}
        # return "ok"

    except Exception as e:
        # print(e)
        return {"error" : f"{e}"}, 400


@app.route("/users/login", methods=["POST"])
def login():
    try:
        user = models.User.query.filter_by(email=request.json["email"]).first()
        # print(user.to_json())

        if not user:
            return {"message": "User not found"}, 401

        elif bcrypt.check_password_hash(user.password, request.json["password"]):
            encrypted_id = jwt.encode(
                {"user_id": user.id}, os.environ.get("JWT_SECRET"), algorithm="HS256"
            )

            return {"user": user.to_json(), "user_id": encrypted_id}

        else:
            return {"message": "password incorrect"}, 402

    except Exception as e:
        return {"error" : f"{e}"}, 400


@app.route("/users/verify", methods=["GET"])
def verify_user():
    try:
        print(request.headers["Authorization"])

        decrypted_id = jwt.decode(
            request.headers["Authorization"],
            os.environ.get("JWT_SECRET"),
            algorithms="HS256",
        )["user_id"]

        # print(f'encrypted_id {request.headers["Authorization"]}')
        print(decrypted_id)

        # user = models.User.query.filter_by(id=request.headers["Authorization"]).first()

        user = models.User.query.filter_by(id=decrypted_id).first()

        if user:
            return {"user": user.to_json()}
        else:
            return {"message": "user not found"}, 401

    except Exception as e:
        print(e)
        return {"error" : f"{e}"}, 400


@app.route("/steam/specials", methods=["GET"])
def get_steam_specials():

    url = "https://store.steampowered.com/search/?sort_by=Released_DESC&tags=-1&specials=2"

    page = requests.get(url).text

    doc = bs(page, "html.parser")

    item_section = doc.find(id="search_resultsRows")

    items = item_section.find_all(class_="responsive_search_name_combined")

    product_list = []
    for item in items:
        try:
            product = item.parent

            product_dict = {}

            product_dict["link"] = product["href"]

            product_dict["name"] = product.find(class_="title").string

            product_dict["original_price"] = product.find(
                class_="col search_price discounted responsive_secondrow"
            ).strike.string

            product_dict["discount_price"] = (
                product.find(
                    class_="col search_price discounted responsive_secondrow")
                .text.split("$")[-1]
                .strip()
            )

            product_dict["discount_percentage"] = product.find(
                class_="col search_discount responsive_secondrow"
            ).text.strip()

            product_dict["image"] = product.find(
                class_="col search_capsule").img["src"]

            product_list.append(product_dict)
        except:
            pass

    return {"products": product_list}


if __name__ == "__main__":
    port = os.environ.get("PORT") or 5001
    app.run("0.0.0.0", port=port, debug=True)
