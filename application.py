import os
from flask import Flask, request
from flask_cors import CORS
import sqlalchemy
from bs4 import BeautifulSoup as bs
import requests
import re

# from testing import testing

from ebay import ebay
from newEgg import new_egg
from Cart import cart
from User import user


app = Flask(__name__)
CORS(app)

from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)


app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
import models

models.db.init_app(app)


# app.register_blueprint(testing)

app.register_blueprint(ebay)

app.register_blueprint(new_egg)

app.register_blueprint(cart)

app.register_blueprint(user)


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
                product.find(class_="col search_price discounted responsive_secondrow")
                .text.split("$")[-1]
                .strip()
            )

            product_dict["discount_percentage"] = product.find(
                class_="col search_discount responsive_secondrow"
            ).text.strip()

            product_dict["image"] = product.find(class_="col search_capsule").img["src"]

            product_list.append(product_dict)
        except:
            pass

    return {"products": product_list}


if __name__ == "__main__":
    port = os.environ.get("PORT") or 5001
    app.run("0.0.0.0", port=port, debug=True)
