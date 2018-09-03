from .site import main, Site


class Kitsu(Site):
    """kitsu.io"""

    BASE_URL = 'https://kitsu.io'
    API_BASE_URL = BASE_URL + '/api/edge'
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
        url = f'{self.API_BASE_URL}/anime/{id}'
        return self._get_json(url)['data']

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
        anime = self._get_json(f'{self.API_BASE_URL}/anime',
                               params=params)['data'][0]

        return int(anime['id'])

    def get_names(self, slug):
        anime = self._get_json(f'{self.API_BASE_URL}/anime',
                               params={'filter[slug]': slug})['data'][0]
        titles = anime['attributes']['titles']

        return {local.replace('_', '-'): title
                for local, title in titles.items()}


if __name__ == '__main__':
    site = Kitsu()
    print(site.get_names('shoujo-kageki-revue-starlight'))
    main(Kitsu(), {'ja-jp': '少女☆歌劇 レヴュースタァライト'})
