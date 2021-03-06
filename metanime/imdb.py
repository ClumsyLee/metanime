import json
import re

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
    SEARCH_LOCALES = ['en-jp', 'en']

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
            'q': name,
            's': 'tt',
            'ttype': 'tv',
        }
        soup = self._get_soup(self.BASE_URL + '/find', params=params)

        regex = re.compile(r'/title/tt(\d+)')
        href = soup.find(class_='article').find('a', href=regex)['href']
        id = int(regex.search(href).group(1))

        return id


if __name__ == '__main__':
    main(IMDB(), {'en-jp': 'Shoujo☆Kageki Revue Starlight'})
