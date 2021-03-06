import re

from .site import main, Site


class WorldArt(Site):
    """world-art.ru"""

    BASE_URL = 'http://www.world-art.ru'
    NAMES = {
        'en': 'WorldArt',
        'ja-jp': 'WorldArt',
        'zh-cn': 'WorldArt',
    }
    MIN_RATING = 1
    MAX_RATING = 10
    SEARCH_LOCALES = ['ja-jp', 'en-jp']

    def info_url(self, id):
        return f'{self.BASE_URL}/animation/animation.php?id={id}'

    def _get_rating(self, id):
        soup = self._get_soup(self.info_url(id))

        rating_str = (soup.find(text='Средний балл').next_element.next_element
                      .get_text())
        rating = float(rating_str.split()[0])

        count_str = (soup.find(text='Проголосовало').next_element.next_element
                     .get_text())
        count = int(count_str.split()[0])

        return rating, count

    def _search(self, name):
        params = {
            'public_search': name.encode('ascii', 'xmlcharrefreplace'),
            'global_sector': 'animation',
        }
        soup = self._get_soup(self.BASE_URL + '/search.php', params=params)

        regex = re.compile(r'animation/animation\.php\?id=(\d+)')

        # Detect whether we were redirected.
        meta = soup.find('meta', content=regex)
        if meta:
            url_str = meta['content']
        else:
            url_str = soup.find('a', href=regex)['href']
        id = int(regex.search(url_str).group(1))

        return id


if __name__ == '__main__':
    main(WorldArt(), {'ja-jp': 'サクラダリセット'})
