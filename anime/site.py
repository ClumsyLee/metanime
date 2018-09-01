from bs4 import BeautifulSoup
import requests


USER_AGENT = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) '
              'AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1.2 '
              'Safari/605.1.15')


class Site(object):
    """Anime site"""

    NAMES = None
    MIN_RATING = None
    MAX_RATING = None

    def __init__(self):
        self.session = requests.Session()
        self.session.headers['User-Agent'] = USER_AGENT

    def _get(self, url, **kws):
        return self.session.get(url, **kws)

    def _post(self, url, **kws):
        return self.session.post(url, **kws)

    def _get_soup(self, url, parser='html5lib', **kws):
        return BeautifulSoup(self._get(url, **kws).text, parser)

    def _get_json(self, url, **kws):
        return self._get(url, **kws).json()

    def _post_json(self, url, json, **kws):
        return self._post(url, json=json, **kws).json()

    def unify_rating(self, rating):
        return int(round((rating - self.MIN_RATING) /
                         (self.MAX_RATING - self.MIN_RATING) * 100))

    def info_url(self, id):
        raise NotImplementedError

    def get_rating(self, id):
        raise NotImplementedError


def main(site, id):
    rating, count = site.get_rating(id)
    unified_rating = site.unify_rating(rating)

    print(site.info_url(id))
    print(f'{rating} ({count}), {unified_rating}')
