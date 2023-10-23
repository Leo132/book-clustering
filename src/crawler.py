'''
Web crawler tools lib

Target websites:
1. https://www.104.com.tw/jobs/search/?ro=0&expansionType=area%2Cspec%2Ccom%2Cjob%2Cwf%2Cwktm&indcat=1001000000&order=16&asc=0&sr=99&rostatus=1024&page=1&mode=s&langFlag=0&langStatus=0&recommendJob=1&hotJob=1 (104 人力銀行)
2. https://www.truemovie.com/tairelease2022.htm (movie)
3. https://www.sanmin.com.tw/promote/top/?id=yy&item=11209&pi=1 (book)
'''

import requests
from bs4 import BeautifulSoup
import json

from typing import Callable

class Parser(BeautifulSoup):
    def __init__(self, markup: str, **kwargs):
        super().__init__(markup, "html.parser", **kwargs)


def get_html_from_url(url: str, method: str="get"):
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
        print(f"Error: request faile. (status code: {r.status_code})")
        return None

    return r.text

def save_info_to_json(page_urls: list[str], folder_file: str, get_urls: Callable,  get_info: Callable):
    def save_to_json(data, path_file):
        with open(path_file, 'w') as f:
            json.dump(data, f)

    for page, page_url in enumerate(page_urls, start=1):
        info_list = []
        print(f"{'page' + str(page):-^60}")
        for idx, url in enumerate(get_urls(page_url), start=1):
            print(url)                         # for debugging
            info = get_info(url)
            if info is None:                   # skip invalid info
                continue
            info_list.append(info)
            print(f"{idx:3d}. {info}")
        save_to_json(info_list, f"./data/{folder_file}{page}.json")
    print("Save success")


# 104 job bank

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

def save_job_to_json():
    job_page_urls = [f"https://www.104.com.tw/jobs/search/?ro=0&expansionType=area%2Cspec%2Ccom%2Cjob%2Cwf%2Cwktm&indcat=1001000000&order=16&asc=0&sr=99&rostatus=1024&page={page + 1}&mode=s&langFlag=0&langStatus=0&recommendJob=1&hotJob=1" for page in range(150)]

    save_info_to_json(job_page_urls, "job_info/job_info_page", get_job_urls, get_job_info)

def _job_test():
    job_page_urls = [f"https://www.104.com.tw/jobs/search/?ro=0&expansionType=area%2Cspec%2Ccom%2Cjob%2Cwf%2Cwktm&indcat=1001000000&order=16&asc=0&sr=99&rostatus=1024&page={page + 1}&mode=s&langFlag=0&langStatus=0&recommendJob=1&hotJob=1" for page in range(150)]

    for page, job_page_url in enumerate(job_page_urls, start=1):
        print(f"{'page ' + str(page):-^80}")
        for idx, url in enumerate(get_job_urls(job_page_url), start=1):
            print(url)                          # for debugging
            job_info = get_job_info(url)
            print(f"{idx:3d}. {job_info}")

# true movie

def get_movie_urls(url: str):
    result = Parser(get_html_from_url(url, "get"))

    return list(map(lambda doc: doc["href"], result.find_all('a', attrs={"style": "text-decoration: none; font-weight: 700"})))

def get_movie_info(url: str):
    from codecs import encode
    # <p style="line-height: 150%"><font face="新細明體"><b>製片預算 / 北美票房：</b>不明</font><font face="新細明體" size="3"> 
	# 	/ 4915萬</font></p>
    result = Parser(get_html_from_url(url))
    text = list(map(lambda doc: doc.string, result.find_all("font", attrs={"face": encode("新細明體", "big5")})))
    print(text)
    # for t in text:
    #     print(t)

def _truemovie_test():
    movie_page_urls = [f"https://www.truemovie.com/tairelease{year}.htm" for year in range(2002, 2024)]

    for movie_page_url in movie_page_urls:
        for idx, movie_url in enumerate(get_movie_urls(movie_page_url)):
            movie_info = get_movie_info(movie_url)
            print(f"{idx:3d}. {movie_info}")

# bookstore

def get_book_urls(url: str):
    result = Parser(get_html_from_url(url))
    book_urls = list(set(url for url in list(map(lambda doc: f"https://www.sanmin.com.tw{doc['href']}", result.find_all('a', attrs={"target": "_parent"})))))
    # for idx, book_url in enumerate(book_urls, start=1):     # for testing
    #     print(f"{idx:3d}. {book_url}")

    return book_urls

def get_book_info(url: str):
    html = get_html_from_url(url)
    if html is None:
        return None
    result = Parser(html)
    div_tag = result.find("div", attrs={"class": "ProductInfo"})
    if div_tag is None:
        print(f"Error: can't find info tag ({url=})")
        return None

    # book name
    book_name = div_tag.contents[1].string

    # book pages
    info_tag = div_tag.contents[3].find_all("li", attrs={"class": "mainText ga"})
    book_pages = None
    for li_tag in info_tag:
        if "頁" in li_tag.text:
            book_pages = int(li_tag.text.split('／')[-1][:-1])
            break
    
    # book publication date
    book_date = None
    for li_tag in info_tag:
        if "出版日" in li_tag.text:
            book_date = li_tag.text[4:]
            break

    # book category
    book_category_list = [] if len(div_tag.contents) < 6 else div_tag.contents[5].find_all('a', attrs={"class": "text-blue bold"})
    book_category = None if len(book_category_list) == 0 else book_category_list[-1].text
    
    # book price
    info_tag = result.find("div", attrs={"class": "mw300 lh-25 m0"}).contents[1]
    for li_tag in info_tag:
        if "定  價" in li_tag.text:
            book_price = int(li_tag.text.replace(' ', '')[7:-1])
            break

    info = {
        "name": book_name,
        "price": book_price,
        "category": book_category,
        "pages": book_pages,
        "date": book_date,
    }

    return info

def save_book_to_json():
    book_page_urls = [f"https://www.sanmin.com.tw/promote/top/?id=yy&item=11209&pi={page + 1}" for page in range(25)]
    # skip those books that are out of print (e.g., page 17 - 334. <王室緋聞守則...>)

    save_info_to_json(book_page_urls, "book_info_/book_info_page", get_book_urls, get_book_info)

def _book_test():
    # book_page_urls = [f"https://www.sanmin.com.tw/promote/top/?id=yy&item=11209&pi={page + 1}" for page in range(25)]

    # for page, book_page_url in enumerate(book_page_urls[:1], start=1):
    #     print(f"{'page' + str(page):-^60}")
    #     for idx, book_url in enumerate(get_book_urls(book_page_url), start=1):
    #         print(book_url)     # for debugging
    #         book_info = get_book_info(book_url)
    #         print(f"{idx:3d}. {book_info}")

    print(get_book_info("https://www.sanmin.com.tw/product/index/012289833"))

# testing

def _test():
    # info_list = get_contact_lense_info([f"./data/web/contact_lenses_page{idx + 1}.html" for idx in range(5)])
    # info_list = get_motor_info([
    #     "https://www.yamaha-motor.com.tw/motor/motorcycle.aspx",
    #     # "https://www.yamaha-motor.com.tw/motor/scooter.aspx"
    # ])

    # for idx, info in enumerate(info_list):
    #     print(f"{idx + 1:3d}. {info}")

    test_url = "https://www.sanmin.com.tw/product/index/010203446"

    _job_test()
    # _truemovie_test()
    # _book_test()
    # save_book_to_json()

    # with open("./src/view.html", 'wb') as f:
    #     f.write(get_html_from_url(test_url, "get").encode("utf-8"))


if __name__ == "__main__":
    _test()