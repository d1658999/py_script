import json

with open('new_bands.json', 'r') as ltemch:
    data = json.load(ltemch)
    print(type(data))
    for k,v in data.items():
        print(k, type(int(k)), v, type(v))