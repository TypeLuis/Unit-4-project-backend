# https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2380057.m570.l1313&_nkw=ps4&_sacat=0

# https://www.ebay.com/sch/i.html?_from=R40&_nkw=3080&_sacat=0&LH_TitleDesc=0

# https://www.ebay.com/sch/i.html?_from=R40&_nkw=3080&_sacat=0&LH_TitleDesc=0&_pgn=9


import requests
from bs4 import BeautifulSoup as bs


from flask import Blueprint, render_template, session, abort, request

ebay = Blueprint("ebay", __name__)


@ebay.route("/ebay/<string:product>", methods=["GET"])
def find_ebay_product(product):

    url = f"https://www.ebay.com/sch/i.html?_from=R40&_nkw={product}&_sacat=0&LH_TitleDesc=0&_pgn={request.args.get('page')}"

    def get_data(url):
        page = requests.get(url).text
        doc = bs(page, "html.parser")
        return doc

    def get_page_num(doc):
        pages = doc.find_all(class_="pagination__item")[-1].text
        print(pages)
        return int(pages)

    def parse(doc):
        results = doc.find_all("div", {"class": "s-item__wrapper clearfix"})
        product_list = []
        for item in results:
            try:
                product = {
                    "image": item.find("img", {"class": "s-item__image-img"})["src"],
                    "title": item.find("h3", {"class": "s-item__title"}).text,
                    "condition": item.find(class_="s-item__subtitle")
                    .find(class_="SECONDARY_INFO")
                    .text,
                    "price": float(
                        item.find("span", {"class": "s-item__price"})
                        .text.replace("$", "")
                        .replace(",", "")
                        .strip()
                    ),
                    "link": item.find("a", {"class": "s-item__link"})["href"].split(
                        "?"
                    )[0],
                }

                if item.find(class_="s-item__shipping s-item__logisticsCost") != None:
                    product["shipping"] = item.find(
                        class_="s-item__shipping s-item__logisticsCost"
                    ).text

                if item.find("span", {"class": "s-item__purchase-options-with-icon"}):
                    product["bidding"] = False
                    product["buying_format"] = item.find(
                        "span", {"class": "s-item__purchase-options-with-icon"}
                    ).text

                elif item.find("span", {"class": "s-item__bids s-item__bidCount"}):
                    product["bidding"] = True
                    product["buying_format"] = item.find(
                        "span", {"class": "s-item__bids s-item__bidCount"}
                    ).text

                product_list.append(product)

            except TypeError as e:
                print(e)
                continue

        return product_list

    doc = get_data(url)
    get_page_num(doc)

    # "pages": get_page_num(doc)
    return {"products": parse(doc), "pages": get_page_num(doc)}
