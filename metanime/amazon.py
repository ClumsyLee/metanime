import re

from .site import main, Site


class Amazon(Site):
    """amazon.com"""

    BASE_URL = 'https://www.amazon.com'
    NAMES = {
        'en': 'Amazon',
        'ja-jp': 'Amazon',
        'zh-cn': '亚马逊',
    }
    MIN_RATING = 1
    MAX_RATING = 5
    SEARCH_LOCALES = ['en']

    def info_url(self, id):
        return f'{self.BASE_URL}/dp/{id}'

    def _get_rating(self, id):
        soup = self._get_soup(self.info_url(id))

        rating_str = soup.find(class_="arp-rating-out-of-text").get_text()
        rating = float(rating_str.strip().split()[0])

        count = int(soup.find(class_="totalReviewCount").get_text())

        return rating, count

    def _search(self, name):
        # Amazon has lots of stuff, so we only match whole words here.
        params = {
            'field-keywords': '"' + name + '"',
            'rh': 'n:2858778011,n:2864549011',
        }
        soup = self._get_soup(self.BASE_URL + '/s', params=params)

        # Handle no results cases.
        if soup.find(id='apsRedirectLink') or soup.find(id='noResultsTitle'):
            raise RuntimeError('No results found')

        regex = re.compile(r'/dp/(\w+)')
        href = soup.find('a', href=regex)['href']
        id = regex.search(href).group(1)

        return id


if __name__ == '__main__':
    main(Amazon(), {'en': 'Dropkick on My Devil!'})
