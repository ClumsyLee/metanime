import re

from .site import main, Site


class Bangumi(Site):
    """bangumi.tv"""

    BASE_URL = 'https://bangumi.tv'
    NAMES = {
        'en': 'Bangumi',
        'ja-jp': 'Bangumi',
        'zh-cn': 'Bangumi',
    }
    MIN_RATING = 1
    MAX_RATING = 10

    def info_url(self, id):
        return f'{self.BASE_URL}/subject/{id}'

    def get_rating(self, id):
        soup = self._get_soup(self.info_url(id))

        rating = float(soup.find(property='v:average').get_text())
        count = int(soup.find(property='v:votes').get_text())

        return rating, count

    def search(self, names):
        soup = self._get_soup(
            self.BASE_URL + '/subject_search/' + names['ja-jp'],
            params={'cat': 2})

        regex = re.compile(r'/subject/(\d+)')
        href = soup.find('a', href=regex)['href']
        id = regex.search(href).group(1)

        return id


if __name__ == '__main__':
    main(Bangumi(), {'ja-jp': '少女☆歌劇 レヴュースタァライト'})
