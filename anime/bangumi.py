from .site import main, Site


class Bangumi(Site):
    """bangumi.tv"""

    NAMES = {
        'en': 'Bangumi',
        'ja-jp': 'Bangumi',
        'zh-cn': 'Bangumi',
    }
    MIN_RATING = 1
    MAX_RATING = 10

    def info_url(self, id):
        return f'https://bangumi.tv/subject/{id}'

    def get_rating(self, id):
        soup = self._get_soup(self.info_url(id))

        rating = float(soup.find(property='v:average').get_text())
        count = int(soup.find(property='v:votes').get_text())

        return rating, count


if __name__ == '__main__':
    main(Bangumi(), '214265')
