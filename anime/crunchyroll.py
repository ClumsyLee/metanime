from .site import main, Site


class Crunchyroll(Site):
    """crunchyroll.com"""

    NAMES = {
        'en': 'Crunchyroll',
        'ja-jp': 'Crunchyroll',
        'zh-cn': 'Crunchyroll',
    }
    MIN_RATING = 1
    MAX_RATING = 5

    def info_url(self, id):
        return f'http://www.crunchyroll.com/{id}'

    def get_rating(self, id):
        soup = self._get_soup(self.info_url(id))

        rating = float(soup.find(itemprop='average').get_text())
        count = int(soup.find(itemprop='votes').get_text())

        return rating, count


if __name__ == '__main__':
    main(Crunchyroll(), 'cells-at-work')
