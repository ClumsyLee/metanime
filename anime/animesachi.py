from .site import main, Site


class Animesachi(Site):
    """animesachi.com"""

    NAMES = {
        'en': 'Animesachi',
        'ja-jp': 'Animesachi',
        'zh-cn': 'Animesachi',
    }
    MIN_RATING = 0
    MAX_RATING = 100

    def info_url(self, id):
        return f'https://www.animesachi.com/visitor/sakuhin_{id}.html'

    def get_rating(self, id):
        soup = self._get_soup(self.info_url(id))
        tds = soup.find('table', class_='normal_2').find_all('td')

        rating = float(tds[4].get_text())
        count = int(tds[24].get_text())

        return rating, count


if __name__ == '__main__':
    main(Animesachi(), '5438')
