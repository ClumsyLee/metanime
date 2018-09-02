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

    def info_url(self, id):
        return f'{self.BASE_URL}/animation/animation.php?id={id}'

    def get_rating(self, id):
        soup = self._get_soup(self.info_url(id))

        rating_str = (soup.find(text='Средний балл').next_element.next_element
                      .get_text())
        rating = float(rating_str.split()[0])

        count_str = (soup.find(text='Проголосовало').next_element.next_element
                     .get_text())
        count = int(count_str.split()[0])

        return rating, count

    def search(self, names):
        params = {
            'public_search': names['ja-jp'].encode('ascii',
                                                   'xmlcharrefreplace'),
            'global_sector': 'animation',
        }
        soup = self._get_soup(self.BASE_URL + '/search.php', params=params)

        regex = re.compile(r'/animation/animation\.php\?id=(\d+)')
        content = soup.find('meta', content=regex)['content']
        id = regex.search(content).group(1)

        return id


if __name__ == '__main__':
    main(WorldArt(), {'ja-jp': 'サクラダリセット'})
