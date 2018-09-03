import re

from .site import main, Site


class Bangumi(Site):
    """bangumi.tv"""

    BASE_URL = 'https://bangumi.tv'
    API_BASE_URL = 'https://api.bgm.tv'
    NAMES = {
        'en': 'Bangumi',
        'ja-jp': 'Bangumi',
        'zh-cn': 'Bangumi',
    }
    MIN_RATING = 1
    MAX_RATING = 10

    def info_url(self, id):
        return f'{self.BASE_URL}/subject/{id}'

    def get_rating(self, id):
        anime = self._get_json(f'{self.API_BASE_URL}/subject/{id}')
        rating = anime['rating']

        return rating['score'], rating['total']

    def search(self, names):
        name = names['ja-jp']
        params = {
            'type': 2,  # Anime.
            'responseGroup': 'small',
            'max_results': 1,
        }
        anime = self._get_json(f'{self.API_BASE_URL}/search/subject/{name}',
                               params=params)['list'][0]

        return anime['id']


if __name__ == '__main__':
    main(Bangumi(), {'ja-jp': '少女☆歌劇 レヴュースタァライト'})
