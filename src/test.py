import json

data = [
        {
        'a': 1,
        'h': 2,
        'c': 3,
        'd': 4,
    }
    for _ in range(5)
]

with open("./data/test.json", 'w') as f:
    json.dump(data, f)