from time import sleep, time

from .site import main, Site


class Saraba1st(Site):
    """saraba1st.com"""

    BASE_URL = 'https://bbs.saraba1st.com'
    NAMES = {
        'en': 'Stage1st',
        'ja-jp': 'Stage1st',
        'zh-cn': 'Stage1st',
    }
    MIN_RATING = -2
    MAX_RATING = 2
    SEARCH_LOCALES = ['ja-jp', 'zh-cn']
    MIN_SEARCH_INTERVAL = 11

    def __init__(self):
        super().__init__()
        self._formhash = None
        self._last_search_epoch = 0

    def info_url(self, id):
        return f'{self.BASE_URL}/2b/thread-{id}-1-1.html'

    def _get_rating(self, id):
        soup = self._get_soup(self.info_url(id))

        counts = [int(node.get_text().strip('()')) for node in
                  soup.select('#poll td em')]
        if len(counts) != 5:
            raise RuntimeError(f'Invalid number of options ({len(counts)})')

        count = sum(counts)
        rating = (2 * counts[0] + counts[1] - counts[3] -
                  2 * counts[4]) / count

        return rating, count

    def _search(self, name):
        if self._formhash is None:
            # Pretend to be on the advance search page.
            soup = self._get_soup(self.BASE_URL +
                                  '/2b/search.php?mod=forum&adv=yes')
            self._formhash = soup.find('input',
                                       attrs={'name': 'formhash'})['value']

        delay = self._last_search_epoch + self.MIN_SEARCH_INTERVAL - time()
        if delay > 0:
            sleep(delay)
        self._last_search_epoch = time()

        data = {
            'formhash': self._formhash,
            'srchtxt': name,
            'srchfilter': 'all',
            'special[]': 1,
            'srchfrom': 0,
            'orderby': 'dateline',
            'ascdesc': 'desc',
            'srchfid[]': '83',
            'searchsubmit': 'yes',
        }
        soup = self._post_soup(self.BASE_URL + '/2b/search.php?mod=forum',
                               data=data)

        id = int(soup.find(class_='pbw')['id'])

        return id


if __name__ == '__main__':
    main(Saraba1st(), {'ja-jp': 'ダーリン・イン・ザ・フランキス',
                       'zh-cn': 'DARLING in the FRANXX'})
