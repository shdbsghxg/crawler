import os

import re
import requests

from bs4 import BeautifulSoup, NavigableString

# location of projects container
PATH_MODULE = os.path.abspath(__file__)
print(f'path_module: {PATH_MODULE}')
ROOT_DIR = os.path.dirname(PATH_MODULE)
print(f'path_module_dir: {ROOT_DIR}')

# location of data/ folder
DATA_DIR = os.path.join(ROOT_DIR, 'data')
print(f'path_data_dir: {DATA_DIR}')


def get_top100_list(refresh_html=False):
    """
    return list of real-time rank01~100
    file location:
        upper dir location based on current location :
            os.path.dirname(os.path.abspath(__nam__))

        rank 01~100: data/chart_realtime_50.html
    :return:
    """

    # if there's no path_data_dir folder, then let it be
    # to make 'path_data_dir = crawler/data' folder
    os.makedirs(DATA_DIR, exist_ok=True)

    # realtime rank url
    url_chart_realtime = 'https://www.melon.com/chart/index.htm'

    # 1.using 'xt' mode and try/except syntax
    #   if refresh_html is True, re-download html source
    file_path = os.path.join(DATA_DIR, 'chart_realtime.html')
    try:
        file_mode = 'wt' if refresh_html else 'xt'
        with open(file_path, file_mode) as f:
            source = requests.get(url_chart_realtime).text
            f.write(source)
    except FileExistsError:
        print(f'"{file_path}" file already exists and up-to-date')

    source = open('melon.html', 'rt').read()
    soup = BeautifulSoup(source, 'lxml')

    result = []
    for tr in soup.find_all('tr', class_=['lst50', 'lst100']):
        rank = tr.find('span', class_='rank').text
        img_src = tr.find('a', class_='image_typeAll').find('img').get('src')
        title = tr.find('div', class_='rank01').find('a').text
        artist = tr.find('div', class_='rank02').find('a').text
        album = tr.find('div', class_='rank03').find('a').text

        # HW review in class
        song_id_href = tr.find('a', class_='song_info').get('href')
        song_id = re.search(r"\('(\d+)'\)", song_id_href).group(1)

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
            'song_id': song_id,

        })

    return result


def get_song_detail(song_id, refresh_html=False):
    """
    terurn details of each songs
    make each elements in 'get_top100_list' get song_id
    ref) http://www.melon.com/song/detail.htm?songId=30755375

    :param song_id:
    :param refresh_html: parameter for checking whether there's HTML already or not
    :return: dict of details
    """

    file_path = os.path.join(DATA_DIR, f'song_detail_{song_id}.html')
    try:
        file_mode = 'wt' if refresh_html else 'xt'
        with open(file_path, file_mode) as f:
            url = f'https://melon.com/song/detail.html'
            params = {
                'songId': song_id,
            }
            response = requests.get(url, params)
            source = response.text
            f.write(source)
    except FileExistsError:
        print(f'"{file_path}" file already exists and up-to-date')
    except ValueError:
        # when file is too short
        os.remove(file_path)
        return

    source = open(file_path, 'rt').read()
    soup = BeautifulSoup(source, 'lxml')

    # div.song_name's child, strong has blanks both side, which is cut by strip()
    # there're multiple ways of extracting data from html by using regex and soup's functions
    title = soup.find('div', class_='song_name').strong.next_sibling.strip()
    div_entry = soup.find('div', class_='entry')
    artist = div_entry.find('div', class_='artist').get_text(strip=True)

    # album, publish_date, genre, etc info as a list
    dl = div_entry.find('div', class_='meta').find('dl')
    items = [item.get_text(strip=True) for item in dl.contents if not isinstance(item, str)]
    it = iter(items)
    description_dict = dict(zip(it, it))

    album = description_dict.get('앨범')
    release_date = description_dict.get('발매일')
    genre = description_dict.get('장르')

    div_lyric = soup.find('div', id='d_video_summary')

    lyrics_list = []
    for item in div_lyric:
        if item.name == 'br':
            lyrics_list.append('\n')
        elif type(item) is NavigableString:
            lyrics_list.append(item.strip())
    lyrics = ''.join(lyrics_list)

    return {
        'title': title,
        'artist': artist,
        'album': album,
        'release_date': release_date,
        'genre': genre,
        'lyrics': lyrics

        # HW
        # 'producer': {
        #     '작사':['별들의 전쟁'],
        #     '작곡':['David Amber', 'Sean Alenxander'],
        #     '편곡':['Avenue52']
        #
        # },
    }


# def song_search(refresh_html=False):
#
#     song_title_search_list = []
#
#     title = input('title to be searched : ')
#     file_path = os.path.join(DATA_DIR, f'song_search_{title}.html')
#
#     try:
#         file_mode = 'wt' if refresh_html else 'xt'
#         with open(file_path, file_mode) as f:
#             url = f'https://www.melon.com/search/total/index.htm?q={title}B&section=&ipath=srch_form'
#             params = {
#                 'title': title,
#             }
#             response = requests.get(url, params)
#             source = response.text
#             f.write(source)
#     except FileExistsError:
#         print(f'"{file_path}" file already exists and up-to-date')
#     except ValueError:
#         # when file is too short
#         os.remove(file_path)
#         return
#
#     source = open(file_path, 'rt').read()
#     soup = BeautifulSoup(source, 'lxml')
#
#     song_title_search = soup.find('div', class_='ellipsis').find('a', class_='fc_gray').get('title')
#
#     song_title_search_list.append({
#         'song_title_search': song_title_search
#     })
#
#     return song_title_search_list

def search_song(q):
    url = 'https://www.melon.com/search/song/index.htm'
    params = {
        'q': q,
        'section': 'song',
    }
    response = requests.get(url, params)
    soup = BeautifulSoup(response.text, 'lxml')
    tr_list = soup.select('form#frm_defaultList table > tbody > tr')

    result = []
    for tr in tr_list:
        q = tr.select_one('td:nth-of-type(3) a.fc_gray').get_text(strip=True)
        artist = tr.select_one('td:nth-of-type(4) span.checkEllipsisSongdefaultList').get_text(strip=True)
        album = tr.select_one('td:nth-of-type(5) a').get_text(strip=True)

        result.append({
            'title': q,
            'artist': artist,
            'album': album,
        })
    return result