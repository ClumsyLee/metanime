import json

from .site import main, Site


class IMDB(Site):
    """imdb.com"""

    BASE_URL = 'https://www.imdb.com'
    NAMES = {
        'en': 'IMDB',
        'ja-jp': 'IMDB',
        'zh-cn': 'IMDB',
    }
    MIN_RATING = 1
    MAX_RATING = 10
    SEARCH_LOCALES = ['en-jp']

    def info_url(self, id):
        return f'{self.BASE_URL}/title/tt{id}'

    def _get_rating(self, id):
        soup = self._get_soup(self.info_url(id))
        json_str = soup.find('script', type='application/ld+json').get_text()
        aggregate_rating = json.loads(json_str)['aggregateRating']

        rating = float(aggregate_rating['ratingValue'])
        count = int(aggregate_rating['ratingCount'])

        return rating, count

    def _search(self, name):
        params = {
            'title': name,
            'title_type': 'tv_series',
        }
        soup = self._get_soup(self.BASE_URL + '/search/title', params=params)

        href = soup.find(class_='lister-item-header').find('a')['href']
        id = int(href.split('/')[2].lstrip('tt'))

        return id


if __name__ == '__main__':
    main(IMDB(), {'en-jp': 'Shoujo☆Kageki Revue Starlight'})
