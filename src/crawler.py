'''
2023/9/23 ~
Web crawler tools lib
'''

import requests
from bs4 import BeautifulSoup

class Parser(BeautifulSoup):
    def __init__(self, markup: str, **kwargs) -> None:
        super().__init__(markup, "html.parser", **kwargs)

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

def _test():
    urls = [
        "https://arxiv.org/",
    ]

    result = Parser(get_html_from_url(urls[0], "a"))
    content = list(map(lambda doc: doc.find("a"), result.find_all("li")))

    for c in content:
        print(c.string)

if __name__ == "__main__":
    _test()