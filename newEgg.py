import requests
from bs4 import BeautifulSoup as bs
from requests_html import HTMLSession
import re


from flask import Blueprint, render_template, session, abort, request

new_egg = Blueprint("newEgg", __name__)


@new_egg.route("/newegg/<string:product>", methods=["GET"])
def find_newegg_product(product):


    if request.args.get("page"):
        #  http://localhost:5000/newegg/am4?page=2
        url = f"https://www.newegg.com/p/pl?d={product}&N=4131&page={request.args.get('page')}"
    else:
        #  http://localhost:5000/newegg/am4
        url = f"https://www.newegg.com/p/pl?d={product}&N=4131"


    session = HTMLSession()
    page = session.get(url).content

    # page = requests.get(url).text

    doc = bs(page, "html.parser")

    # finds the pagination element
    page_text = doc.find('span', class_="list-tool-pagination-text").strong

    # pages = int(doc.find_all(class_='btn-group-cell')[-2].button.text)

    # splits to get the last page number
    pages = int(str(page_text).split("/")[-2].split(">")[-1][:-1])

    items_found = {}

    div = doc.find(
        class_="item-cells-wrap border-cells items-grid-view four-cells expulsion-one-cell"
    )

    # finds all element that has the same text as the product

    # re.compile(product, re.I) finds element even if it's case sensative or has more characters inside the text element
    items = div.find_all(text=re.compile(str(product), re.I))

    for item in items:
        parent = item.parent  # the parent of the item element is an <a> tag
        if parent.name != "a":
            continue

        link = parent["href"]

        short_link = link.split("?")[0].split("/")[-1]

        product_div = item.find_parent(class_="item-container")

        try:
            price = product_div.find(class_="price-current").strong.string
            image = product_div.img["src"]
            # print(price)
            items_found[item] = {
                "price": int(price.replace(",", "")),
                "link": link,
                "image": image,
                "short_link": short_link,
            }
        except:
            pass

    sorted_items = sorted(items_found.items(), key=lambda x: x[1]["price"])

    # print("LHUIEHUIFHUI", items_found.items())

    sorted_list = []
    for item in sorted_items:
        sorted_dict = {
            "name": item[0],
            "price": str(item[1]["price"]),
            "link": item[1]["link"],
            "image": item[1]["image"],
            "short_link": item[1]["short_link"],
        }

        sorted_list.append(sorted_dict)
    # print(sorted_list)

    return {f"products": sorted_list, "pages": pages}


@new_egg.route("/newegg/page/<string:url>", methods=["GET"])
def newegg_product_page(url):
    try:
        # http://localhost:5001/newegg/page?N82E16834156031
        page = requests.get(f"https://www.newegg.com/p/{url}").text
        #
        doc = bs(page, "html.parser")
        page_dict = {}

        bullet_points = doc.find(class_="product-bullets").find_all("li")
        product_bullets = []
        for bullet in bullet_points:
            bullet_dict = {"bullet_point": bullet.string.strip()}
            product_bullets.append(bullet_dict)
            # print(item.string)

        page_dict["product_list"] = product_bullets

        product_modules = doc.find_all(class_="a-plus-module")
        modules = []
        for module in product_modules:
            module_dict = {}
            if module.img:
                # print(module.img["src"].replace("//", ""))
                module_dict["image"] = module.img["src"].replace("//", "")

            if module.p:
                module_dict["text"] = module.p.string

            if module.img or module.p:
                modules.append(module_dict)

        page_dict["overview"] = modules

        image_divs = doc.find_all(class_="swiper-zoom-container")
        images = []
        for div in image_divs:
            image_dict = {}
            if div.img and "CompressAll" not in div.img["src"]:
                image_dict["image"] = div.img["src"]
                images.append(image_dict)

        page_dict["images"] = images

        spec_divs = doc.find_all(class_="table-horizontal")
        specs = []

        for div in spec_divs:

            if div.caption.string != None:
                spec_dict = {"caption": div.caption.string}
            else:
                spec_dict = {}

            trs = div.tbody.contents
            for row in trs:
                header, data = row.contents
                # print(str(header))
                header = header.text
                # header = str(header).split(">")[1].split("<")[0]
                data = str(data).split("td>")[1].split("</td")[0]
                if "<br/>" in data:
                    data = data.replace("<br/>", "\n")
                    print(data)
                spec_dict["header"] = header
                spec_dict["data"] = data.replace("</", "")

            specs.append(spec_dict)

        page_dict["specs"] = specs

        return {"page_info": page_dict}

    except Exception as e:
        print(e)
        return {"error" f"{e}"}, 400
