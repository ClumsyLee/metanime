import re
from statistics import mean

from .site import main, Site


class Reddit(Site):
    """reddit.com/r/anime"""

    BASE_URL = 'https://www.reddit.com/r/anime'
    NAMES = {
        'en': 'Reddit',
        'ja-jp': 'Reddit',
        'zh-cn': 'Reddit',
    }
    MIN_RATING = 1
    MAX_RATING = 10
    DYNAMIC_ID = True
    SEARCH_LOCALES = ['en-jp', 'en']

    def info_url(self, id):
        return f'{self.BASE_URL}/comments/{id}'

    def _get_post(self, id):
        return (self._get_json(self.info_url(id) + '.json')[0]['data']
                ['children'][0]['data'])

    def _get_poll_rating(self, poll_id):
        soup = self._get_soup(f'https://youpoll.me/{poll_id}/r')

        rating = float(soup.find(class_='rating-mean-value').get_text())
        count = int(soup.find(class_='admin-total-votes').get_text())

        return rating, count

    def _get_rating(self, id):
        text = self._get_post(id)['selftext']
        poll_ids = re.findall(r'youpoll\.me/(\d+)', text)
        link_ids = re.findall(r'redd\.it/(\w+)', text)

        if len(poll_ids) != len(link_ids) + 1:
            raise RuntimeError(f'Number of polls ({len(poll_ids)}) != '
                               f'number of links ({len(link_ids)}) + 1')

        ratings = []
        counts = []

        for poll_id in poll_ids:
            rating, count = self._get_poll_rating(poll_id)
            ratings.append(rating)
            counts.append(count)

        return mean(ratings), int(mean(counts))

    def _search(self, name):
        # AutoLovepon usually use numbers instead of words.
        name = name.lower()
        name = name.replace('1st', '1').replace('first', '1')
        name = name.replace('2nd', '2').replace('second', '2')
        name = name.replace('3rd', '3').replace('third', '3')

        params = {
            'q': 'author:AutoLovepon ' + name,
            'restrict_sr': 'on',
            'sort': 'new',
            't': 'all',
        }
        post = self._get_json(self.BASE_URL + '/search.json',
                              params=params)['data']['children'][0]['data']

        return post['id']


if __name__ == '__main__':
    main(Reddit(), {'en-jp': 'Shoujo☆Kageki Revue Starlight'})
