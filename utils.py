import os

import re
import requests

from bs4 import BeautifulSoup

source = open('melon.html', 'rt').read()
soup = BeautifulSoup(source, 'lxml')


def get_top100_list(refresh_html=False):
    """
    return list of real-time rank01~100
    file location:
        upper dir location based on current location :
            os.path.dirname(os.path.abspath(__nam__))

        rank 01~100: data/chart_realtime_50.html
    :return:
    """

    # location of projects container
    path_module = os.path.abspath(__name__)
    print(f'path_module: {path_module}')
    root_dir = os.path.dirname(path_module)
    print(f'path_module_dir: {root_dir}')

    # location of data/ folder
    path_data_dir = os.path.join(root_dir, 'data')
    print(f'path_data_dir: {path_data_dir}')

    # if there's no path_data_dir folder, then let it be
    # to make 'path_data_dir = crawler/data' folder
    os.makedirs(path_data_dir, exist_ok=True)

    # realtime rank url
    url_chart_realtime = 'https://www.melon.com/chart/index.htm'

    # 1.using 'xt' mode and try/except syntax
    #   if refresh_html is True, re-download html source
    file_path = os.path.join(path_data_dir, 'chart_realtime.html')
    try:
        file_mode = 'wt' if refresh_html else 'xt'
        with open(file_path, file_mode) as f:
            source = requests.get(url_chart_realtime).text
            f.write(source)
    except FileExistsError:
        print(f'"{file_path}" file already exists and up-to-date')

    result = []
    for tr in soup.find_all('tr', class_=['lst50', 'lst100']):
        rank = tr.find('span', class_='rank').text
        img_src = tr.find('a', class_='image_typeAll').find('img').get('src')
        title = tr.find('div', class_='rank01').find('a').text
        artist = tr.find('div', class_='rank02').find('a').text
        album = tr.find('div', class_='rank03').find('a').text
        # .* -> 임의 문자 최대 반복
        # \. -> '.' 문자
        # .*?/ -> '/' 전까지 임의 문자 최소 반복
        p = re.compile(r'(.*\..*?)/')
        img_src = re.search(p, img_src).group(1)

        result.append({
            'rank': rank,
            'img_src': img_src,
            'title': title,
            'artist': artist,
            'album': album,
        })

    return result
