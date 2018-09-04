from .site import main, Site


class Shikimori(Site):
    """shikimori.org"""

    BASE_URL = 'https://shikimori.org'
    NAMES = {
        'en': 'Shikimori',
        'ja-jp': 'Shikimori',
        'zh-cn': 'Shikimori',
    }
    MIN_RATING = 1
    MAX_RATING = 10

    def info_url(self, id):
        return f'{self.BASE_URL}/animes/{id}'

    def _get_rating(self, id):
        info = self._get_json(f'{self.BASE_URL}/api/animes/{id}')

        rating = float(info['score'])
        count = sum(entry['value'] for entry in info['rates_scores_stats'])

        return rating, count

    def _search(self, name):
        params = {
            'search': name,
            'kind': 'tv',
            'limit': 1,
        }
        info = self._get_json(self.BASE_URL + '/api/animes', params=params)[0]

        return info['id']


if __name__ == '__main__':
    main(Shikimori(), {'ja-jp': '少女☆歌劇 レヴュースタァライト'})
