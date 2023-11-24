'''
Clustering algorithm tools lib
'''

from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import MinMaxScaler
from sklearn.pipeline import Pipeline

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

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

def visualize(data: pd.DataFrame, cluster: list[int], is_2d: bool=True):
    dim = 2 if is_2d else 3
    points = [data.iloc[:, i] for i in range(dim)]
    labels = data.columns

    fig = plt.figure()
    ax = fig.add_subplot(projection=None if is_2d else '3d')
    scatter = ax.scatter(*points, c=cluster)
    set_labels = [
        ax.set_xlabel,
        ax.set_ylabel,
        None if is_2d else ax.set_zlabel,
    ]
    for set_label, label in zip(set_labels, labels):
        set_label(label)
    plt.legend(*scatter.legend_elements(), title="Classes")
    
    plt.show()


def _test():
    from utils import load_json, unionize_jsons, extract_features

    # load data
    print("data loading...")
    # features, _ = make_blobs(
    #     n_samples=200,
    #     centers=3,
    #     cluster_std=2.75,
    #     random_state=42
    # )
    col = ["price", "pages", "date"]
    data = load_json("./data/book_info.json")
    # data = unionize_jsons([f"./data/book_info/book_info_page{page + 1}.json" for page in range(25)], "name")
    data, features = extract_features(data, col)

    # clustering
    kmeans_kwargs = {
        "init": "k-means++",
        "n_init": 10,
        "max_iter": 300,
        # "random_state": 42,
    }
    is_dev = False

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

        df = pd.DataFrame(
            pipe["preprocessor"].transform(features),
            columns=col
        )

        visualize(df, pipe["clusterer"]["kmeans"].labels_, len(col) == 2)



if __name__ == "__main__":
    _test()