import json

from .site import main, Site


class IMDB(Site):
    """imdb.com"""

    NAMES = {
        'en': 'IMDB',
        'ja-jp': 'IMDB',
        'zh-cn': 'IMDB',
    }
    MIN_RATING = 1
    MAX_RATING = 10

    def info_url(self, id):
        return f'https://www.imdb.com/title/{id}'

    def get_rating(self, id):
        soup = self._get_soup(self.info_url(id))
        json_str = soup.find('script', type='application/ld+json').get_text()
        aggregate_rating = json.loads(json_str)['aggregateRating']

        rating = float(aggregate_rating['ratingValue'])
        count = int(aggregate_rating['ratingCount'])

        return rating, count


if __name__ == '__main__':
    main(IMDB(), 'tt8400680')
