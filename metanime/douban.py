import re

from .site import main, Site


class Douban(Site):
    """douban.com"""

    BASE_URL = 'https://movie.douban.com'
    API_BASE_URL = 'https://api.douban.com/v2/movie'
    NAMES = {
        'en': 'Douban',
        'ja-jp': 'Douban',
        'zh-cn': '豆瓣',
    }
    MIN_RATING = 2
    MAX_RATING = 10
    SEARCH_LOCALES = ['ja-jp', 'zh-cn']

    def info_url(self, id):
        return f'{self.BASE_URL}/subject/{id}'

    # def _get_rating(self, id):
    #     anime = self._get_json(f'{self.API_BASE_URL}/subject/{id}')
    #     return anime['rating']['average'], anime['ratings_count']

    def _get_rating(self, id):
        soup = self._get_soup(self.info_url(id))

        rating = float(soup.find(property='v:average').get_text())
        count = int(soup.find(property='v:votes').get_text())

        return rating, count

    # def _search(self, name):
    #     anime = self._get_json(f'{self.API_BASE_URL}/search',
    #                            params={'q': name})['subjects'][0]
    #     return int(anime['id'])

    def _search(self, name):
        params = {
            'cat': 1002,
            'q': name,
        }
        soup = self._get_soup('https://www.douban.com/search', params=params)

        href = soup.find(class_='title').find('a')['href']
        id = int(re.search(r'subject%2F(\d+)', href).group(1))

        return id


if __name__ == '__main__':
    main(Douban(), {'ja-jp': '少女☆歌劇 レヴュースタァライト'})
