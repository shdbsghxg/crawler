
import os
import requests


def get_top100_list():
    """
    return list of real-time rank01~100
    file location:
        upper dir location based on current location :
            os.path.dirname(os.path.abspath(__nam__))

        rank 01~50: data/chart_realtime_50.html
        rank 51~100: data/chart_realtime_100.html
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
    url_chart_realtime_50 = 'https://www.melon.com/chart/index.htm'
    url_chart_realtime_100 = 'https://www.melon.com/chart/index.htm#params%5Bidx%5D=51'

    # 1.using 'xt' mode and try/except syntax
    file_path_50 = os.path.join(path_data_dir, 'chart_realtime_50.html')
    try:
        with open(file_path_50, 'wt') as f:
            source50 = requests.get(url_chart_realtime_50).text
            f.write(source50)
    except FileExistsError:
        print(f'"{file_path}" file already exists')

    # 2. check before sending a requests
    file_path_100 = os.path.join(path_data_dir, 'chart_realtime_100.html')
    if not os.path.exists(file_path_100,):
        with open(file_path_100, 'wt') as f:
            source100 = requests.get(url_chart_realtime_100).text
            f.write(source100)
    source = source50 + source100











    # file_path = os.path.join(path_data_dir, 'chart_realtime_50.html')
    # with open(file_path, 'wt') as f:
    #     response = requests.get(url_chart_realtime_50)
    #     source = response.text
    #     f.write(source)
    #
    # file_path = os.path.join(path_data_dir, 'chart_realtime_100.html')
    # with open(file_path, 'wt') as f:
    #     response = requests.get(url_chart_realtime_100)
    #     source = response.text
    #     f.write(source)
    #
    #
    # result = []
    # for tr in soup.find_all('tr', class_='lst50'):
    #     rank = tr.find('span', class_='rank').text
    #     img_src = tr.find('img').get('src')
    #     title = tr.find('div', class_='rank01').find('a').text
    #     artist = tr.find('div', class_='rank02').find('a').text
    #     album = tr.find('div', class_='rank03').find('a').text
    #     # .* -> 임의 문자 최대 반복
    #     # \. -> '.' 문자
    #     # .*?/ -> '/' 전까지 임의 문자 최소 반복
    #     p = re.compile(r'.*(\..*?)/')
    #     img_src = re.search(p, img_src).group(1)
    #
    #     result.append({
    #         'rank': rank,
    #         'img_src': img_src,
    #         'title': title,
    #         'artist': artist,
    #         'album': album,
    #
    #     })
    #
