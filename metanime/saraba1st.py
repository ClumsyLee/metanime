from .site import main, Site


class Saraba1st(Site):
    """saraba1st.com"""

    BASE_URL = 'https://bbs.saraba1st.com'
    NAMES = {
        'en': 'Saraba1st',
        'ja-jp': 'Saraba1st',
        'zh-cn': 'Saraba1st',
    }
    MIN_RATING = -2
    MAX_RATING = 2

    def __init__(self):
        super().__init__()
        self._formhash = None

    def info_url(self, id):
        return f'{self.BASE_URL}/2b/thread-{id}-1-1.html'

    def get_rating(self, id):
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

    def search(self, names):
        try:
            return self._search(names['ja-jp'])
        except Exception:
            pass

        return self._search(names['zh-cn'])


if __name__ == '__main__':
    main(Saraba1st(), {'ja-jp': 'ダーリン・イン・ザ・フランキス',
                       'zh-cn': 'DARLING in the FRANXX'})
