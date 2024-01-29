import json

with open('storage/data.json', 'r', encoding='utf-8') as json_file:
    a = json_file.read()
    b = json_file.read()
    print('a: ', a)
    print('b: ', b)