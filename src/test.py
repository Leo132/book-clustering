import json

data = {
    'a': 1,
    'h': 2,
    'c': 3,
    'd': 4,
}
x = [n for n in range(10)]
y = [n*2 for n in range(10)]

for xi, yi in zip(*[x, y]):
    print(xi, yi)