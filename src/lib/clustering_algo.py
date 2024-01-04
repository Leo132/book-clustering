'''
Clustering algorithm tools lib

Features:
    price           : int
    pages           : int
    published_date  : int
'''

from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import MinMaxScaler
from sklearn.pipeline import Pipeline

import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt

from utils import load_json, save_to_json, extract_features

def make_pipeline(k: int, init: str, n_init: int, max_iter: int):
    preprocessor = Pipeline(
        [("scaler", MinMaxScaler())]
    )
    clusterer = Pipeline(
        [
            (
                "kmeans",
                KMeans(
                    n_clusters=k,
                    init=init,
                    n_init=n_init,
                    max_iter=max_iter,
                )
            )
        ]
    )

    return Pipeline(
        [
            ("preprocessor", preprocessor),
            ("clusterer", clusterer)
        ]
    )

def visualize(data: pd.DataFrame, clusters: list[int], is_2d: bool=True, file_name: str=None):
    dim = 2 if is_2d else 3
    points = [data.iloc[:, i] for i in range(dim)]
    labels = data.columns

    fig = plt.figure()
    ax = fig.add_subplot(projection=None if is_2d else '3d')
    scatter = ax.scatter(*points, c=clusters)
    set_labels = [
        ax.set_xlabel,
        ax.set_ylabel,
        None if is_2d else ax.set_zlabel,
    ]
    for set_label, label in zip(set_labels, labels):
        set_label(label)
    plt.legend(*scatter.legend_elements(), title="Clusters")
    
    if file_name is None:
        plt.show()
    else:
        plt.savefig(file_name)

def plot_cluster_num():
    clusters_n = [cluster["book_num"] for cluster in sorted(load_json("./data/cluster_info.json"), key=lambda cluster: cluster["cluster_id"])]
    cluster_names = [f"群{idx + 1}" for idx in range(len(clusters_n))]
    plt.bar(cluster_names, clusters_n)
    plt.grid(True)
    plt.show()

def plot_clustering_analysis(cols: list[str], cols_ch: list[str], file_name: str=None):
    book_info_ = sorted(load_json("./data/book_info.json"), key=lambda info: info["cluster"])
    cluster_table = {cluster + 1: [] for cluster in range(8)}
    for info in book_info_:
        cluster_table[info["cluster"]].append(info)
    book_info = []
    centers = []
    # for cluster in range(1, 9):
    for cluster in [2, 5, 8]:
        book_info += cluster_table[cluster]
        data, _ = extract_features(cluster_table[cluster], cols)
        centers.append([sum(data[col])/len(data[col]) for col in cols])
    clusters = [info["cluster"] for info in book_info] + [0]*len(centers)
    # data = unionize_jsons([f"./data/book_info/book_info_page{page + 1}.json" for page in range(25)], "name")
    data, features = extract_features(book_info, cols)
    print(len(book_info), len(features))
    for cluster, center in enumerate(centers, start=1):
        print(cluster, center)

    scaler = MinMaxScaler()
    norm_features = scaler.fit_transform(features + centers)
    # norm_features = scaler.fit_transform(features)
    df = pd.DataFrame(norm_features, columns=cols_ch)

    visualize(df, clusters, len(cols) == 2, file_name)

def clustering(book_info: list[str], features: list[list], cols: list[str], /, is_dev: bool=False, save_result: bool=True, display: bool=False):
    # clustering
    kmeans_kwargs = {
        "init": "k-means++",
        "n_init": 20,
        "max_iter": 300,
        # "random_state": 42,
    }

    if is_dev:
        n = 15
        sse = []

        for k in range(1, n + 1):
            print(f"iter: {k:2d}", end='')
            pipe = make_pipeline(k, **kmeans_kwargs)
            pipe.fit(features)

            kmeans = pipe["clusterer"]["kmeans"]
            print(f", loss: {kmeans.inertia_:10.5f}")
            sse.append(kmeans.inertia_)

        plt.plot(range(1, n + 1), sse)
        plt.show()
    else:
        k = 8
        pipe = make_pipeline(k, **kmeans_kwargs)
        pipe.fit(features)

        df = pd.DataFrame(pipe["preprocessor"].transform(features), columns=cols)
        result = pipe["clusterer"]["kmeans"]
        labels = result.labels_
        cluster_centers = pipe["preprocessor"].inverse_transform(result.cluster_centers_)
        print(cluster_centers)

        # save clustering result
        if save_result:
            from collections import Counter
            counter = Counter(labels)
            print(counter)
            print(labels)
            cluster_info = [{
                "cluster_id": label.item() + 1,
                "book_num": num,
                "average_price": round(cluster_centers[label][0], 2),
                "average_pages": round(cluster_centers[label][1], 2),
                "average_time": round(cluster_centers[label][2], 2),
            } for label, num in counter.items()]
            for info, label in zip(book_info, labels):
                info["cluster"] = label.item() + 1
            save_to_json(book_info, "./data/book_info.json")
            for info in cluster_info:
                print(info)
            save_to_json(cluster_info, "./data/cluster_info.json")
        if display:
            visualize(df, labels, len(cols) == 2)

def plot_category_analysis():
    book_info = load_json("./data/book_info.json")
    categories = load_json("./data/category.json")["category"]
    category_counts = {
        cluster_id: {category: 0 for category in categories}
        for cluster_id in range(1, 9)
    }

    for info in book_info:
        category_counts[info["cluster"]][info["category"]] += 1
    
    for cluster_id, categories_count in category_counts.items():
        plt.figure(figsize=(14, 4))
        plt.bar(categories_count.keys(), categories_count.values())
        plt.title(f"Cluster {cluster_id} (total: {sum(categories_count.values())})")
        plt.grid(True)
        plt.savefig(f"./data/img/category_analysis_cluster{cluster_id}.png")
        plt.clf()

def _test():

    # load data
    print("data loading...")
    # features, _ = make_blobs(
    #     n_samples=200,
    #     centers=3,
    #     cluster_std=2.75,
    #     random_state=42
    # )

    # Chinese font setting
    plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei'] 
    plt.rcParams['axes.unicode_minus'] = False
    # matplotlib.rcParams.update({'font.size': 22})

    # -- plot "cluster_num.png"
    # plot_cluster_num()

    # -- plot "clustering_analysis.png"
    # cols = ["price", "pages", "published_date"]             # consider all features
    # plot_clustering_analysis(cols, ["價錢", "頁數", "時間"])

    # cols = ["price", "pages"]                               # consider only two features
    # plot_clustering_analysis(cols, ["價錢", "頁數"], f"./data/img/result_only_two_features ({', '.join(cols)})")

    # cols = ["price", "published_date"]                      # consider only two features
    # plot_clustering_analysis(cols, ["頁數", "時間"], f"./data/img/result_only_two_features ({', '.join(cols)})")

    # cols = ["pages", "published_date"]                      # consider only two features
    # plot_clustering_analysis(cols, ["價錢", "時間"], f"./data/img/result_only_two_features ({', '.join(cols)})")

    # -- plot "result.png"
    # cols = ["price", "pages", "published_date"]
    # book_info = load_json("./data/book_info.json")
    # data, features = extract_features(book_info, cols)
    # clustering(book_info, features, cols, save_result=False, display=True)

    # -- plot "category_analysis.png"
    plot_category_analysis()

if __name__ == "__main__":
    _test()