from bs4 import BeautifulSoup
from xml.etree import ElementTree
import requests


USER_AGENT = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) '
              'AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1.2 '
              'Safari/605.1.15')


class Site(object):
    """Anime site"""

    BASE_URL = None
    NAMES = None
    MIN_RATING = None
    MAX_RATING = None
    DYNAMIC_ID = False
    SEARCH_LOCALES = ['ja-jp']

    def __init__(self):
        self.session = requests.Session()
        self.session.headers['User-Agent'] = USER_AGENT

    def _get(self, url, **kws):
        return self.session.get(url, **kws)

    def _post(self, url, **kws):
        return self.session.post(url, **kws)

    def _get_soup(self, url, parser='html5lib', **kws):
        return BeautifulSoup(self._get(url, **kws).text, parser)

    def _post_soup(self, url, parser='html5lib', **kws):
        return BeautifulSoup(self._post(url, **kws).text, parser)

    def _get_json(self, url, **kws):
        return self._get(url, **kws).json()

    def _post_json(self, url, json, **kws):
        return self._post(url, json=json, **kws).json()

    def _get_xml(self, url, **kws):
        return ElementTree.fromstring(self._get(url, **kws).content)

    def unify_rating(self, rating):
        return int(round((rating - self.MIN_RATING) /
                         (self.MAX_RATING - self.MIN_RATING) * 100))

    def get_rating(self, id):
        try:
            return self._get_rating(id)
        except Exception:
            return None, None

    def search(self, names):
        for locale in self.SEARCH_LOCALES:
            if locale in names:
                try:
                    return self._search(names[locale])
                except Exception:
                    pass  # No worries, just try next locale.

        return None

    def info_url(self, id):
        raise NotImplementedError

    def _get_rating(self, id):
        raise NotImplementedError

    def _search(self, name):
        raise NotImplementedError


def main(site, names):
    id = site.search(names)
    if id is None:
        return

    print(site.info_url(id))

    rating, count = site.get_rating(id)
    if rating is not None:
        unified_rating = site.unify_rating(rating)
    else:
        unified_rating = None

    print(f'{rating} ({count}), {unified_rating}')
