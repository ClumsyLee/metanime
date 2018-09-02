import re

from .site import main, Site


class Douban(Site):
    """douban.com"""

    BASE_URL = 'https://movie.douban.com'
    NAMES = {
        'en': 'Douban',
        'ja-jp': 'Douban',
        'zh-cn': '豆瓣',
    }
    MIN_RATING = 2
    MAX_RATING = 10

    def info_url(self, id):
        return f'{self.BASE_URL}/subject/{id}'

    def get_rating(self, id):
        soup = self._get_soup(self.info_url(id))

        rating = float(soup.find(property='v:average').get_text())
        count = int(soup.find(property='v:votes').get_text())

        return rating, count

    def search(self, names):
        params = {
            'cat': 1002,
            'q': names['ja-jp'],
        }
        soup = self._get_soup('https://www.douban.com/search', params=params)

        href = soup.find(class_='title').find('a')['href']
        id = re.search(r'subject%2F(\d+)', href).group(1)

        return id


if __name__ == '__main__':
    main(Douban(), {'ja-jp': '少女☆歌劇 レヴュースタァライト'})
