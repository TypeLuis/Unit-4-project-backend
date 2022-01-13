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
                    "short_link": item.find("a", {"class": "s-item__link"})["href"]
                    .split("?")[0]
                    .split("/")[-1],
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

            except Exception as e:
                print(e)
                continue

        return product_list

    doc = get_data(url)
    get_page_num(doc)

    # "pages": get_page_num(doc)
    return {"products": parse(doc), "pages": get_page_num(doc)}


@ebay.route("/ebay/page/<string:url>", methods=["GET"])
def ebay_product_page(url):
    try:
        url = f"https://www.ebay.com/itm/{url}"

        def get_data(url):
            page = requests.get(url).text
            doc = bs(page, "html.parser")
            return doc

        def parse(doc):
            page_dict = {}
            title = doc.find("h1", {"id": "itemTitle"}).text
            if "Details about" in title:
                page_dict["title"] = title.split("Details about")[-1].strip()


            if '/ea' in doc.find(id="prcIsum"):
                page_dict["price"] = float(
                    doc.find(id="prcIsum")
                    .text.split(" ")[-1]
                    .replace("$", "")
                    .replace(",", "")
                ).split('/')[0]

            else:
                page_dict["price"] = float(
                    doc.find(id="prcIsum")
                    .text.split(" ")[-1]
                    .replace("$", "")
                    .replace(",", "")
                )

            page_dict["image"] = doc.find(id="icImg")["src"]

            if doc.find("iframe", {"id": "desc_ifr"}):
                iframe = doc.find("iframe", {"id": "desc_ifr"})["src"]
                frame_page = requests.get(iframe).text

                frame_doc = bs(frame_page, "html.parser")

                frame_doc.title.decompose()

                for s in frame_doc.select("script"):
                    s.extract()

                page_dict["description_page"] = frame_doc.text.strip()

                # frame_doc = frame_doc.script.decompose()  # this removes all script tags in doc

                # images = frame_doc.find_all("div", {"class": "g_image fimage"})

                # for image in images:
                #     if image["data"]:
                #         print(image["data"])

                return page_dict

        doc = get_data(url)

        return {"page_info": parse(doc)}

    except Exception as e:
        print(e)
        return {"page_info": f'{e}'}
