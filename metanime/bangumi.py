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
    SEARCH_LOCALES = ['ja-jp', 'zh-cn', 'en-jp', 'en']

    def info_url(self, id):
        return f'{self.BASE_URL}/subject/{id}'

    def _get_rating(self, id):
        anime = self._get_json(f'{self.API_BASE_URL}/subject/{id}')
        rating = anime['rating']

        return rating['score'], rating['total']

    def _get_anime_by_name(self, name):
        name = name.replace('-', ' ').replace('!', ' ')
        params = {
            'type': 2,  # Anime.
            'responseGroup': 'small',
            # 'max_results': 1,  # Would cause a bug on "ISLAND"
        }
        return self._get_json(f'{self.API_BASE_URL}/search/subject/{name}',
                              params=params)['list'][0]

    def _search(self, name, update_names=False):
        anime = self._get_anime_by_name(name)
        return anime['id']

    def get_zh_cn_name(self, name):
        try:
            return self._get_anime_by_name(name)['name_cn']
        except Exception:
            return None


if __name__ == '__main__':
    main(Bangumi(), {'ja-jp': '少女☆歌劇 レヴュースタァライト'})
