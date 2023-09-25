'''
2023/9/23 ~
Web crawler tools lib

Target website:
1. https://www.eyesmart.com.tw/category/35/0/5/1/ (隱形眼鏡)
2. 
'''

import requests
from bs4 import BeautifulSoup

from datatype import ContactLense

class Parser(BeautifulSoup):
    def __init__(self, markup: str, **kwargs):
        super().__init__(markup, "html.parser", **kwargs)


def get_html_from_url(url: str, method: str="get"):
    try:
        r = {
            "get": requests.get,
            "post": requests.post
        }[method](url)
    except KeyError as e:
        print(f"{type(e).__name__}: `method` should be 'get' or 'post', but '{e}' was given")
        return

    if r.status_code != 200:
        return None
    
    return r.text

def get_contact_lense_info(file_pathes: list[str]):
    info_list = []

    for file_path in file_pathes:
        with open(file_path, encoding="utf-8") as f:
            result = Parser(f)
        
        content = result.find_all('a', attrs={"dataectype": "clickProduct"})

        for c in content:
            cycle, water_content, diameter, price = list(map(lambda doc: doc.string, c.find_all("span")))[:4]
            name = c.find("div", class_="product_name").string
            info_list.append(ContactLense(name, cycle, water_content, diameter, int(price)).info())

    return info_list

def get_motor_info(urls: list[str]):
    info_list = []

    for url in urls:
        result = Parser(get_html_from_url(url, "get"))
        product_urls = list(map(lambda doc: "https://www.yamaha-motor.com.tw" + doc["href"], result.find_all('a', attrs={"class": ""})))[3:-13]
        results = [Parser(get_html_from_url(product_url, "get")) for product_url in product_urls]
        for result in results[:1]:
            print(result)               # `result` -> view.html (line 1258: empty...)
        # content = list(map(lambda doc: {doc["th"]: doc["td"]}, result.find_all("tr", attrs={})))
        # content = [list(map(lambda doc: doc, result.find_all("thead", attrs={"id": "comparehead"}))) for result in results]
        # for c in content:
        #     print(c)

    return info_list

def _test():
    # info_list = get_contact_lense_info([f"./data/web/contact_lenses_page{idx + 1}.html" for idx in range(5)])
    info_list = get_motor_info([
        "https://www.yamaha-motor.com.tw/motor/motorcycle.aspx",
        # "https://www.yamaha-motor.com.tw/motor/scooter.aspx"
    ])

    for idx, info in enumerate(info_list):
        print(f"{idx + 1:3d}. {info}")

if __name__ == "__main__":
    _test()