import json
from datetime import date

from typing import Callable

class WSModel:
    def __init__(self):
        self._model = None

    def load_model(self):
        if self._model is not None:
            return
        print("Importing ckiptagger...")
        from ckiptagger import WS

        print("Loading model...")
        self._model = WS("./model/data")
        print("Ready!")
    
    def inference(self, input_: str):
        if self._model is None:
            print("Error: model isn't loaded.")
            return input_
        print("Inferencing...")
        return self._model([input_])[0]

# for json

def save_to_json(data: list[dict], path_file: str):
    with open(path_file, 'w', encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)

def save_info_to_json(page_urls: list[str], folder_file: str, get_urls: Callable,  get_info: Callable):
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

# --
def save_author_info_to_json(data: list[str], folder_file: str,  get_info: Callable):
    info_list = []
    page = 1
    for idx, url in enumerate(data, start=1):
        print(url)                         # for debugging
        info = get_info(url)
        info["name"]
        if info is None:                   # skip invalid info
            continue
        info_list.append(info)
        print(f"{idx:3d}. {info}")
        if idx%25 == 0:
            save_to_json(info_list, f"./data/{folder_file}{page}.json")
            page += 1
            info_list = []
    print("Save success")

# split the author_data
def split_data(data: list):
    change_data = [item for element in data for item in element.split(';')]
    seen_elements = set()
    result_array = []
    for element in change_data:
        # 使用 split 方法分割元素，然後選擇第一部分
        parts = element.split('-')
        truncated_element = parts[0]

        # 如果截斷後的元素不在集合中，則將其添加到結果陣列和集合中
        if truncated_element not in seen_elements:
            result_array.append(truncated_element)
            seen_elements.add(truncated_element)
    
    return result_array
# --

def load_json(path_file: str):
    with open(path_file) as f:
        data = json.load(f)
    
    return data

# avoid duplicate data
def unionize_jsons(path_files: list[str], identifier: str):
    table = set()
    data = []

    for path_file in path_files:
        data_ = load_json(path_file)
        for d in data_:
            if d[identifier] in table:
                continue
            data.append(d)
            table.add(d[identifier])
    
    return data

# for book info

def get_all_attrs(data: list[dict], attrs: list[str], is_split: bool = True):
    return [[d[attr] for d in data] for attr in attrs] if is_split else {attr: [d[attr] for d in data] for attr in attrs}

# for clustering

def extract_features(data: list[dict], col: list[str]):
    def is_valid(info: dict, col: list[str]):
        for c in col:
            if c == "published_date" and info[c] is not None:
                continue
            if not isinstance(info[c], int) and not isinstance(info[c], float):
                return False
        
        return True

    data_ = {k: [] for k in data[0].keys()}

    for d in data:
        if not is_valid(d, col):
            continue
        for k, v in d.items():
            if k == "published_date":
                v = (date.today() - date(*list(map(int, v.split('/'))))).days
            data_[k].append(v)
    
    features = [list(d) for d in zip(*[data_[c] for c in col])]

    return data_, features


def _test():
    import os

    # path = "./data/phouse_info"
    # entries = os.scandir(path)
    # path_files = [f"{path}/{file.name}" for file in entries]
    books = load_json(f"./data/book_info.json")
    # phouses = load_json(f"./data/phouse_info.json")
    # authors = load_json("./data/author_info.json")
    clusters = load_json(f"./data/cluster_info.json")

    # print(len(books), len(authors), len(phouses))

    for cluster in clusters:
        cluster_data = [info for info in books if info["cluster"] == cluster["cluster_id"]]
        data, _ = extract_features(cluster_data, ["price", "pages", "published_date"])
        price, pages, published_date = data["price"], data["pages"], data["published_date"]
        avg = lambda x: round(sum(x)/len(x), 2)
        def mean(x):
            x.sort()
            size = len(x)
            return x[size//2] if size % 2 != 0 else avg(x[size//2:size//2 + 2])
        kv = {
            "average_price": avg(price),
            "average_pages": avg(pages),
            "average_time": avg(published_date),
            "mean_price": mean(price),
            "mean_pages": mean(pages),
            "mean_time": mean(published_date),
            "categories": list(set([info["category"] for info in cluster_data])),
        }
        print(kv["categories"])
        for key, val in kv.items():
            cluster[key] = val
    save_to_json(clusters, "./data/cluster_info_.json")

    # table = list(set(get_all_attrs(data, ["category"])[0]))
    # print(table)
    # valid_json = {"category": table}
    # save_to_json(valid_json, "./data/category.json")
    
    # save_to_json(data, f"{path}.json")
    # authors, phouses, isbns = get_all_attrs(data, ["author", "phouse", "ISBN13"])
    # print(len(authors), len(phouses), len(isbns))
    
    # data, features = extract_features(data, ["price", "pages", "date"])

    # for k, v in data.items():
    #     print(k, v)
    # for f in features[:5]:
    #     print(f)
    # print(len(features))

if __name__ == "__main__":
    _test()