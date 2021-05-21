import json
import os
from bs4 import BeautifulSoup

if __name__ == '__main__':
    JSONS_DIR = 'jsons'
    DOCS_DIR = 'docs'
    DATA_DIR = 'data'
    fileno = 0
    docs = []
    for json_file in os.listdir(JSONS_DIR):
        if not json_file.endswith('.json'):
            continue

        with open(os.path.join(JSONS_DIR, json_file), 'r') as file:
            data = json.load(file)
            for doc in data:
                docs.append({'link': doc['link'], 'name': doc['name']})

                text = doc['article']
                cleantext = BeautifulSoup(text, 'lxml').text

                filename = os.path.join('..', DOCS_DIR, 'doc' + str(fileno).zfill(5) + '.txt')
                with open(filename, 'w', encoding='utf-8') as to_write:
                    to_write.write(cleantext)
                fileno += 1

    with open(os.path.join('..', DATA_DIR, 'docs.json'), 'w') as json_file:
        json.dump(docs, json_file)
