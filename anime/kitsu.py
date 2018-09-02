from .site import main, Site


class Kitsu(Site):
    """kitsu.io"""

    BASE_URL = 'https://kitsu.io'
    NAMES = {
        'en': 'Kitsu',
        'ja-jp': 'Kitsu',
        'zh-cn': 'Kitsu',
    }
    MIN_RATING = 5
    MAX_RATING = 100

    def info_url(self, id):
        return f'{self.BASE_URL}/anime/{id}'

    def _get_anime(self, id):
        url = f'{self.BASE_URL}/api/edge/anime?&filter%5Bslug%5D={id}'
        return self._get_json(url)['data'][0]

    def get_rating(self, id):
        attrs = self._get_anime(id)['attributes']

        rating = float(attrs['averageRating'])
        count = sum(int(value) for value in
                    attrs['ratingFrequencies'].values())

        return rating, count

    def search(self, names):
        params = {
            'filter[text]': names['ja-jp'],
            'page[limit]': 1,
        }
        attrs = self._get_json(self.BASE_URL + '/api/edge/anime',
                               params=params)['data'][0]['attributes']

        return attrs['slug']


if __name__ == '__main__':
    main(Kitsu(), {'ja-jp': '少女☆歌劇 レヴュースタァライト'})
