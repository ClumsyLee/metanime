import re
from statistics import mean

from .site import main, Site


class Reddit(Site):
    """reddit.com/r/anime"""

    NAMES = {
        'en': 'Reddit',
        'ja-jp': 'Reddit',
        'zh-cn': 'Reddit',
    }
    MIN_RATING = 1
    MAX_RATING = 10

    def info_url(self, id):
        return f'https://www.reddit.com/r/anime/comments/{id}'

    def _get_info(self, id):
        return (self._get_json(self.info_url(id) + '.json')[0]['data']
                ['children'][0]['data'])

    def _get_poll_rating(self, poll_id):
        soup = self._get_soup(f'https://youpoll.me/{poll_id}/r')

        rating = float(soup.find(class_='rating-mean-value').get_text())
        count = int(soup.find(class_='admin-total-votes').get_text())

        return rating, count

    def get_rating(self, id):
        info = self._get_info(id)
        ratings = []
        counts = []

        for m in re.finditer(r'youpoll\.me/(\d+)', info['selftext']):
            rating, count = self._get_poll_rating(m.group(1))
            ratings.append(rating)
            counts.append(count)

        return mean(ratings), int(mean(counts))


if __name__ == '__main__':
    main(Reddit(), '9a6pjj')
