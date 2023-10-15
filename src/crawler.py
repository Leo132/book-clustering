'''
Web crawler tools lib

Target websites:
1. https://www.104.com.tw/jobs/search/?ro=0&expansionType=area%2Cspec%2Ccom%2Cjob%2Cwf%2Cwktm&indcat=1001000000&order=16&asc=0&sr=99&rostatus=1024&page=1&mode=s&langFlag=0&langStatus=0&recommendJob=1&hotJob=1 (104 人力銀行)
2. 
'''

import requests
from bs4 import BeautifulSoup

class Parser(BeautifulSoup):
    def __init__(self, markup: str, **kwargs):
        super().__init__(markup, "html.parser", **kwargs)


def get_html_from_url(url: str, method: str):
    header = {
    }
    try:
        r = {
            "get": requests.get,
            "post": requests.post
        }[method](url, headers=header)
    except KeyError as e:
        print(f"{type(e).__name__}: `method` should be 'get' or 'post', but '{e}' was given")
        return None

    if r.status_code != 200:
        print(f"Request failed. (status code: {r.status_code})")
        return None

    return r.text


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

# 104 人力銀行

def get_job_urls(url: str):
    result = Parser(get_html_from_url(url, "get"))
    job_urls = list(map(lambda doc: f"https:{doc['href']}", result.find_all('a', attrs={"class": "js-job-link"})))

    return job_urls

def get_job_info(url: str):
    def extract_salary_from_text(text: str):
        # skip 時薪、待遇面議 and 論件計酬
        if text[1:3] != "月薪":
            return None

        # print(text[3:text.rfind('0') + 1])  # for debugging
        s = list(map(lambda s: int(s.replace(',', '')), text[3:text.rfind('0') + 1].split('~')))
        return s + (s if len(s) < 2 else [])
    
    result = Parser(get_html_from_url(url, "get"))
    salary_text = result.find('p', attrs={"class": "t3 mb-0 mr-2 text-primary font-weight-bold align-top d-inline-block"}).string
    title = result.find("h1", attrs={"class": "pr-6 text-break"})["title"]

    info = {
        "title": title,
        "salary": extract_salary_from_text(salary_text),
    }

    return info

def _job_test():
    job_page_urls = [f"https://www.104.com.tw/jobs/search/?ro=0&expansionType=area%2Cspec%2Ccom%2Cjob%2Cwf%2Cwktm&indcat=1001000000&order=16&asc=0&sr=99&rostatus=1024&page={page + 1}&mode=s&langFlag=0&langStatus=0&recommendJob=1&hotJob=1" for page in range(150)]

    for page, job_page_url in enumerate(job_page_urls, start=1):
        print(f"{'page ' + str(page):-^80}")
        for idx, url in enumerate(get_job_urls(job_page_url), start=1):
            # print(url)
            job_info = get_job_info(url)
            print(f"{idx:2d}. {job_info}")

def _test():
    # info_list = get_contact_lense_info([f"./data/web/contact_lenses_page{idx + 1}.html" for idx in range(5)])
    # info_list = get_motor_info([
    #     "https://www.yamaha-motor.com.tw/motor/motorcycle.aspx",
    #     # "https://www.yamaha-motor.com.tw/motor/scooter.aspx"
    # ])

    # for idx, info in enumerate(info_list):
    #     print(f"{idx + 1:3d}. {info}")

    test_url = "https://c.8891.com.tw/Models/ford"

    with open("./src/view.html", 'wb') as f:
        f.write(get_html_from_url(test_url, "get").encode("utf-8"))


if __name__ == "__main__":
    _test()
    # import urllib.request as req
    # import json

    # url = "https://www.yamaha-motor.com.tw/api/comparelist.ashx"
    # model = "YZF-R7"
    # res = req.Request(url, headers={
    #     "type": "post",
    #     "url": "../api/comparelist.ashx",
    #     "data": f"v=1&model={model}",
    #     # "dataType": "json",
    #     "content-length": 16,
    #     "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
    # })
    # # with req.urlopen(res) as response:
    # #     data = json.load(response)
    # x = req.urlopen(res, timeout=10)
    # raw_data = x.read()
    # encoding = x.info().get_content_charset('utf8')  # JSON default
    # # data = json.loads(raw_data.decode(encoding))
    # print(f"'{raw_data.decode(encoding)}'")