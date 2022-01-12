# from flask import Blueprint, render_template, session, abort

# testing = Blueprint("testing", __name__)


# @testing.route("/test", methods=["GET"])
# def test():
#     return "it works!"


# testing.route("/test", methods=["GET"])(test)
import requests
from bs4 import BeautifulSoup as bs

url = f"https://www.ebay.com/itm/133939568717"


def get_data(url):
    page = requests.get(url).text
    doc = bs(page, "html.parser")
    return doc


def parse(doc):
    page_dict = {}
    title = doc.find("h1", {"id": "itemTitle"}).text
    if "Details about" in title:
        page_dict["title"] = title.split("Details about")[-1].strip()

    page_dict["price"] = float(
        doc.find(id="prcIsum").text.split(" ")[-1].replace("$", "").replace(",", "")
    )

    page_dict["image"] = doc.find(id="icImg")["src"]

    iframes = doc.find_all("iframe")

    print(iframes)

    if doc.find("iframe", {"id": "desc_ifr"}):
        iframe = doc.find("iframe", {"id": "desc_ifr"})["src"]
        frame_page = requests.get(iframe).text

        frame_doc = bs(frame_page, "html.parser")

        frame_doc.title.decompose()

        for s in frame_doc.select("script"):
            s.extract()

        page_dict["description_page"] = str(frame_doc).strip()

        # frame_doc = frame_doc.script.decompose()  # this removes all script tags in doc

        # images = frame_doc.find_all("div", {"class": "g_image fimage"})

        # for image in images:
        #     if image["data"]:
        #         print(image["data"])

        print(page_dict)


doc = get_data(url)
parse(doc)
