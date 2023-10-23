import json


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
    path_files = [f"./data/book_info/book_info_page{page + 1}.json" for page in range(25)]
    # data = load_json("./data/book_info/book_info_page1.json")
    data = unionize_jsons(path_files, "name")

    # for d in data:
    #     print(d)
    
    data, features = extract_features(data, ["price", "pages"])

    # for k, v in data.items():
    #     print(k, v)
    for f in features[:5]:
        print(f)
    print(len(features))

if __name__ == "__main__":
    _test()