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

    def info_url(self, id):
        return f'{self.BASE_URL}/subject/{id}'

    def get_rating(self, id):
        anime = self._get_json(f'{self.API_BASE_URL}/subject/{id}')

        return anime['rating']['average'], anime['ratings_count']

    def search(self, names):
        anime = self._get_json(f'{self.API_BASE_URL}/search',
                               params={'q': names['ja-jp']})['subjects'][0]

        return int(anime['id'])


if __name__ == '__main__':
    main(Douban(), {'ja-jp': '少女☆歌劇 レヴュースタァライト'})
