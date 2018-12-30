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
    SEARCH_LOCALES = ['ja-jp', 'en-jp', 'en']

    def info_url(self, id):
        return f'{self.BASE_URL}/anime/{id}'

    def _get_anime(self, id):
        url = f'{self.API_BASE_URL}/anime/{id}'
        return self._get_json(url)['data']

    def _get_anime_by_slug(self, slug):
        url = f'{self.API_BASE_URL}/anime'
        return self._get_json(url, params={'filter[slug]': slug})['data'][0]

    def _get_rating(self, id):
        attrs = self._get_anime(id)['attributes']

        rating = float(attrs['averageRating'])
        count = sum(int(value) for value in
                    attrs['ratingFrequencies'].values())

        return rating, count

    def _search(self, name):
        params = {
            'filter[text]': name,
            'page[limit]': 1,
        }
        anime = self._get_json(f'{self.API_BASE_URL}/anime',
                               params=params)['data'][0]

        return int(anime['id'])

    def search_by_slug(self, slug):
        return int(self._get_anime_by_slug(slug)['id'])

    def get_names(self, slug):
        titles = self._get_anime_by_slug(slug)['attributes']['titles']
        titles = {local.replace('_', '-'): title
                  for local, title in titles.items()}

        # Remove en-us.
        if 'en-us' in titles:
            if 'en' not in titles:
                titles['en'] = titles['en-us']
            del titles['en-us']

        return titles


if __name__ == '__main__':
    site = Kitsu()
    print(site.get_names('shoujo-kageki-revue-starlight'))
    main(Kitsu(), {'ja-jp': '少女☆歌劇 レヴュースタァライト'})
