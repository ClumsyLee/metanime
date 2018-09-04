from .site import main, Site


class Bilibili(Site):
    """bilibili.com"""

    BASE_URL = 'https://www.bilibili.com'
    API_BASE_URL = 'https://bangumi.bilibili.com/view/web_api'
    NAMES = {
        'en': 'Bilibili',
        'ja-jp': 'ビリビリ',
        'zh-cn': '哔哩哔哩',
    }
    MIN_RATING = 2
    MAX_RATING = 10
    SEARCH_LOCALES = ['ja-jp', 'zh-cn']

    def info_url(self, id):
        return f'{self.BASE_URL}/bangumi/media/md{id}'

    def _get_rating(self, id):
        anime = self._get_json(f'{self.API_BASE_URL}/season',
                               params={'media_id': id})['result']
        rating = anime['rating']

        return float(rating['score']), int(rating['count'])

    def _search(self, name):
        params = {
            'search_type': 'media_bangumi',
            'keyword': name,
        }
        media = self._get_json(
            'https://api.bilibili.com/x/web-interface/search/type',
            params=params)['data']['result'][0]

        return media['media_id']


if __name__ == '__main__':
    main(Bilibili(), {'ja-jp': '少女☆歌劇 レヴュースタァライト'})
