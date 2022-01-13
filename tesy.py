from bs4 import BeautifulSoup as bs
import requests
import flask_sqlalchemy

print(flask_sqlalchemy)

page = requests.get(
    "https://www.newegg.com/gigabyte-x570-aorus-elite-wifi/p/N82E16813145165?Item=N82E16813145165&cm_sp=Homepage_SS-_-P1_13-145-165-_-01102022"
).text

doc = bs(page, "html.parser")
page_dict = {}


bullet_points = doc.find(class_="product-bullets").find_all("li")
product_bullets = []
for bullet in bullet_points:
    bullet_dict = {"bullet-point": bullet.string.strip()}
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
        header = str(header).split(">")[1].split("<")[0]
        data = str(data).split("td>")[1].split("</td")[0]
        if "<br/>" in data:
            data = data.replace("<br/>", "\n")
            print(data)
        spec_dict["header"] = header
        spec_dict["data"] = data.replace("</", "")

    specs.append(spec_dict)

page_dict["specs"] = specs

print(page_dict)
