'''
2023/9/23 ~
Web crawler tools lib
'''

import requests
from bs4 import BeautifulSoup

from datatype import ContactLense

class Parser(BeautifulSoup):
    def __init__(self, markup: str, **kwargs) -> None:
        super().__init__(markup, "html.parser", **kwargs)
    
    # def find_all(tag: str, class_: str):
    #     return __class__(super().find_all(tag, class_=class_))

def get_html_from_url(url: str, method: str="get"):
    try:
        r = {
            "get": requests.get,
            "post": requests.post
        }[method](url)
    except KeyError as e:
        print(f"{type(e).__name__}: `method` should be 'get' or 'post', but {e} was given")
        return

    if r.status_code != 200:
        return None
    
    return r.text

def get_contact_lense_info(file_pathes: list[str]):
    info_list = []

    for file_path in file_pathes:
        with open(file_path, encoding="utf-8") as f:
            result = Parser(f)
        
        content = list(map(lambda doc: doc, result.find_all('a', attrs={"dataectype": "clickProduct"})))

        for c in content:
            cycle, water_content, diameter, price = list(map(lambda doc: doc.string, c.find_all("span")))[:4]
            name = c.find("div", class_="product_name").string
            info_list.append(ContactLense(name, cycle, water_content, diameter, int(price)).info())

    return info_list

def _test():
    urls = [
        "https://arxiv.org/",
    ]

    info_list = get_contact_lense_info([f"./data/web/contact_lenses_page{idx + 1}.html" for idx in range(5)])
    for idx, info in enumerate(info_list):
        print(f"{idx + 1:3d}. {info}")

if __name__ == "__main__":
    _test()