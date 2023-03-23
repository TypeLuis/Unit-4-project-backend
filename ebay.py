# https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2380057.m570.l1313&_nkw=ps4&_sacat=0

# https://www.ebay.com/sch/i.html?_from=R40&_nkw=3080&_sacat=0&LH_TitleDesc=0

# https://www.ebay.com/sch/i.html?_from=R40&_nkw=3080&_sacat=0&LH_TitleDesc=0&_pgn=9


import requests
from bs4 import BeautifulSoup as bs


from flask import Blueprint, render_template, session, abort, request

ebay = Blueprint("ebay", __name__)


# This Route gets data of the products requested from ebay
@ebay.route("/ebay/<string:product>", methods=["GET"])
def find_ebay_product(product):

    url = f"https://www.ebay.com/sch/i.html?_from=R40&_nkw={product}&_sacat=0&LH_TitleDesc=0&_pgn={request.args.get('page')}"

    # This returns the html document of the url
    def get_data(url):
        page = requests.get(url).text
        doc = bs(page, "html.parser")
        return doc

    # This gets the amount of pages available
    def get_page_num(doc):
        # finds the last item in pagination item which is the last page
        pages = doc.find_all(class_="pagination__item")[-1].text
        return int(pages)

    # This parses through each product that's available
    def parse(doc):
        results = doc.find_all("div", {"class": "s-item__wrapper clearfix"})
        product_list = []
        for item in results:
            try:

                product = {}

                # product['image'] = item.find("img", {"class": "s-item__image-img"})["src"]
                product['image'] = item.find(
                    "div", {"class": "s-item__image"}).find('img')['src']

                product['title'] = item.find(
                    "div", {"class": "s-item__title"}).text

                product['condition'] = item.find(
                    class_="s-item__subtitle").find(class_="SECONDARY_INFO").text

                # product['price'] = float(item.find(
                #     "span", {"class": "s-item__price"}).text.replace("$", "").replace(",", "").strip())

                if 'Shop on eBay' in product['title']:
                    continue

                product['link'] = item.find(
                    "a", {"class": "s-item__link"})["href"].split("?")[0]

                product['short_link'] = item.find(
                    "a", {"class": "s-item__link"})["href"].split("?")[0].split("/")[-1]

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
            title = doc.find("h1", {"class": "x-item-title__mainTitle"}).text
            print(title)
            if "Details about" in title:
                page_dict["title"] = title.split("Details about")[-1].strip()

            page_dict["price"] = float(doc.find(
                "span", {"itemprop": "price"})['content'])

            page_dict["image"] = doc.find(
                "img", {"itemprop": "image"})["src"]

            if doc.find("iframe", {"id": "desc_ifr"}):
                try:
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

                except Exception as e:
                    pass
            return page_dict

        doc = get_data(url)

        return {"page_info": parse(doc)}

    except Exception as e:
        print(e)
        return {"page_info": f'{e}'}
