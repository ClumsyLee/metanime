from .site import main, Site


class Kitsu(Site):
    """kitsu.io"""

    NAMES = {
        'en': 'Kitsu',
        'ja-jp': 'Kitsu',
        'zh-cn': 'Kitsu',
    }
    MIN_RATING = 5
    MAX_RATING = 100

    def info_url(self, id):
        return f'https://kitsu.io/anime/{id}'

    def _get_info(self, id):
        url = ('https://kitsu.io/api/edge/anime?fields%5Bcategories%5D=slug&'
               f'filter%5Bslug%5D={id}')
        return self._get_json(url)['data'][0]

    def get_rating(self, id):
        attrs = self._get_info(id)['attributes']

        rating = float(attrs['averageRating'])
        count = sum(int(value) for value in
                    attrs['ratingFrequencies'].values())

        return rating, count


if __name__ == '__main__':
    main(Kitsu(), 'shoujo-kageki-revue-starlight')
