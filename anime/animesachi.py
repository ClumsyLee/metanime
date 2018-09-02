import re

from .site import main, Site


class Animesachi(Site):
    """animesachi.com"""

    BASE_URL = 'https://www.animesachi.com'
    NAMES = {
        'en': 'Animesachi',
        'ja-jp': 'Animesachi',
        'zh-cn': 'Animesachi',
    }
    MIN_RATING = 0
    MAX_RATING = 100

    def info_url(self, id):
        return f'{self.BASE_URL}/visitor/sakuhin_{id}.html'

    def get_rating(self, id):
        soup = self._get_soup(self.info_url(id))
        tds = soup.find('table', class_='normal_2').find_all('td')

        rating = float(tds[4].get_text())
        count = int(tds[24].get_text())

        return rating, count

    def search(self, names):
        soup = self._get_soup(self.BASE_URL + '/visitor/search.php',
                              params={'key': names['ja-jp']})

        regex = re.compile(r'sakuhin_(\d+)\.html')
        href = soup.find('a', href=regex)['href']
        id = regex.search(href).group(1)

        return id


if __name__ == '__main__':
    main(Animesachi(), {'ja-jp': '少女☆歌劇 レヴュースタァライト'})
