import json

from typing import Callable

# for json

def save_to_json(data: list[dict], path_file: str):
    with open(path_file, 'w') as f:
        json.dump(data, f)

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
    return [list(set(d[attr] for d in data)) for attr in attrs] if is_split else {attr: list(set(d[attr] for d in data)) for attr in attrs}

# for clustering
def extract_features(data:  dict, col: list[str]):
    def is_valid(info: dict, col: list[str]):
        for c in col:
            if not isinstance(info[c], int) and not isinstance(info[c], float):
                return False
        
        return True

    data_ = {k: [] for k in data[0].keys()}

    for d in data:
        if not is_valid(d, col):
            continue
        for k, v in d.items():
            data_[k].append(v)
    
    features = [list(d) for d in zip(*[data_[c] for c in col])]

    return data_, features


def _test():
    # path_files = [f"./data/book_info/book_info_page{page + 1}.json" for page in range(25)]
    data = load_json("./data/book_info.json")
    # data = unionize_jsons(path_files, "name")

    # for idx, d in enumerate(data, start=1):
    #     print(idx, d)
    
    # save_to_json(data, "./data/book_info.json")
    authors, phouses, isbns = get_all_attrs(data, ["author", "phouse", "ISBN13"])
    print(len(authors), len(phouses), len(isbns))
    
    # data, features = extract_features(data, ["price", "pages"])

    # for k, v in data.items():
    #     print(k, v)
    # for f in features[:5]:
    #     print(f)
    # print(len(features))

if __name__ == "__main__":
    _test()