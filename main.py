import re
from bs4 import BeautifulSoup

from utils import get_top100_list

source = open('melon.html', 'rt').read()
soup = BeautifulSoup(source, 'lxml')

result = []
for tr in soup.find_all('tr', class_='lst50'):
    rank = tr.find('span', class_='rank').string
    img_src = tr.find('img').get('src')
    title = tr.find('div', class_='rank01').find('a').string
    artist = tr.find('div', class_='rank02').find('a').string
    album = tr.find('div', class_='rank03').find('a').string
    # .* -> 임의 문자 최대 반복
    # \. -> '.' 문자
    # .*?/ -> '/' 전까지 임의 문자 최소 반복
    p = re.compile(r'.*(\..*?)/')
    img_src = re.search(p, img_src).group(1)

    result.append({
        'rank' : rank,
        'img_src' : img_src,
        'title' : title,
        'artist' : artist,
        'album' : album,

    })
    # print(title)
    # print(artist)
    # print(album)
    # print(img_src)

if __name__ == '__main__':
    result = get_top100_list()
    # for item in result:
    #     print(item)