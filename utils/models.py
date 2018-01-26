
import os
import requests

from bs4 import BeautifulSoup, NavigableString

# location of projects container
PATH_MODULE = os.path.abspath(__file__)

ROOT_DIR = os.path.dirname(os.path.dirname(PATH_MODULE))

# location of data/ folder
DATA_DIR = os.path.join(ROOT_DIR, 'data')


class MelonCrawler:

    def search_song(self, q):
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
            song_id = tr.select_one('td:nth-of-type(1) input[type=checkbox]').get('value')
            title = tr.select_one('td:nth-of-type(3) a.fc_gray').get_text(strip=True)
            artist = tr.select_one('td:nth-of-type(4) span.checkEllipsisSongdefaultList').get_text(strip=True)
            album = tr.select_one('td:nth-of-type(5) a').get_text(strip=True)

            song = Song(song_id=song_id, title=title, artist=artist, album=album)
            result.append(song)

        return result


class Song:
    def __init__(self, song_id, title, artist, album):
        self.song_id = song_id
        self.title = title
        self.artist = artist
        self.album = album

        self._release_date = None
        self._lyrics = None
        self._genre = None
        self._producers = None

        # self.title = MelonCrawler.search_song(title)
        # self.artist = MelonCrawler.search_song(title).get('artist')
        # self.album = MelonCrawler.search_song(title).get('album')

    def __str__(self):
        return f'{self.title} (아티스트: {self.artist}, 앨범: {self.album})'

    def get_detail(self, refresh_html=False):
        """
        fill in _release_date, _lyrics, _genre, _product
        :return:
        """
        file_path = os.path.join(DATA_DIR, f'song_detail_{self.song_id}.html')
        try:
            file_mode = 'wt' if refresh_html else 'xt'
            with open(file_path, file_mode) as f:
                url = f'https://melon.com/song/detail.html'
                params = {
                    'songId': self.song_id,
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

        self.title = title
        self.artist = artist
        self.album = album

        self._release_date = release_date
        self._genre = genre
        self._lyrics = lyrics
        self._producers = {}

    @property
    def lyrics(self):
        if not self._lyrics:
            self.get_detail()
        return self._lyrics
