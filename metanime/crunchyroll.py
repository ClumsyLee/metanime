import json

from .site import main, Site


class Crunchyroll(Site):
    """crunchyroll.com"""

    BASE_URL = 'https://www.crunchyroll.com'
    NAMES = {
        'en': 'Crunchyroll',
        'ja-jp': 'Crunchyroll',
        'zh-cn': 'Crunchyroll',
    }
    MIN_RATING = 1
    MAX_RATING = 5

    def __init__(self):
        super().__init__()

        self._search_candidates = self._get_search_candidates()

    def info_url(self, id):
        return f'{self.BASE_URL}/{id}'

    def _get_search_candidates(self):
        result = self._get(self.BASE_URL +
                           '/ajax/?req=RpcApiSearch_GetSearchCandidates').text
        json_str = result[result.find('{'):result.rfind('}') + 1]
        data = json.loads(json_str)['data']

        return {entry['name'].lower(): entry['link'].lstrip('/')
                for entry in data
                if entry['type'] == 'Series' and entry['name'] is not None}

    def get_rating(self, id):
        soup = self._get_soup(self.info_url(id))

        rating = float(soup.find(itemprop='average').get_text())
        count = int(soup.find(itemprop='votes').get_text())

        return rating, count

    def search(self, names):
        return self._search_candidates[names['en'].lower()]


if __name__ == '__main__':
    main(Crunchyroll(), {'en': 'Cells at Work!'})
