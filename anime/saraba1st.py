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

    def search(self, names):
        params = {
            'mod': 'forum',
            'searchid': 282,
            'orderby': 'lastpost',
            'ascdesc': 'desc',
            'searchsubmit': 'yes',
            'kw': names['ja-jp'],
        }
        soup = self._get_soup(self.BASE_URL + '/2b/search.php', params=params)

        id = soup.find(class_='pbw')['id']

        return id


if __name__ == '__main__':
    main(Saraba1st(), {'ja-jp': 'サクラダリセット'})
