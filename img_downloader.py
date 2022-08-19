import os
import csv
import urllib.request

opener = urllib.request.build_opener()
opener.addheaders = [
    ('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
urllib.request.install_opener(opener)


BRANDS = [
    'rolex',
    'omega',
    'tagheuer',
    'seiko',
    'patekphilippe',
    'cartier',
    'iwc',
    'jaegerlecoultre',
    'vacheronconstantin',
    'hamilton',
    'oris',
    'audemarspiguet',
    'tudor',
    'longines',
    'richardmille',
]

for brand in BRANDS:
    os.makedirs(f'data/images/{brand}', exist_ok=True)
    with open(f'data/scraped/{brand}.csv', newline='') as file:
        reader = csv.reader(file, delimiter=',')
        index = 0
        for row in reader:
            #print(row[0], index, row[1])
            urllib.request.urlretrieve(
                row[0], f'data/images/{brand}/{brand}-{index}-{row[1]}.jpg')
            index += 1
    print(f'{brand} images saved!')
