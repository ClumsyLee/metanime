import json
import re

from .site import main, Site


class Shinden(Site):
    """shinden.pl"""

    BASE_URL = 'https://shinden.pl'
    NAMES = {
        'en': 'Shinden',
        'ja-jp': 'Shinden',
        'zh-cn': 'Shinden',
    }
    MIN_RATING = 1
    MAX_RATING = 10
    SEARCH_LOCALES = ['ja-jp', 'en-jp']

    def info_url(self, id):
        return f'{self.BASE_URL}/series/{id}'

    def _get_rating(self, id):
        soup = self._get_soup(self.info_url(id))
        json_str = soup.body.find('script',
                                  type='application/ld+json').get_text()
        aggregate_rating = json.loads(json_str)['aggregateRating']

        rating = float(aggregate_rating['ratingValue'])
        count = int(aggregate_rating['reviewCount'])

        return rating, count

    def _search(self, name):
        params = {
            'search': name,
            'series_type[0]': 'TV',
        }
        soup = self._get_soup(self.BASE_URL + '/series', params=params)

        regex = re.compile(r'/series/(\d+)')
        href = soup.find('article').find('a', href=regex)['href']
        id = int(regex.search(href).group(1))

        return id


if __name__ == '__main__':
    main(Shinden(), {'ja-jp': '少女☆歌劇 レヴュースタァライト'})
