from .site import main, Site


class WorldArt(Site):
    """world-art.ru"""

    NAMES = {
        'en': 'WorldArt',
        'ja-jp': 'WorldArt',
        'zh-cn': 'WorldArt',
    }
    MIN_RATING = 1
    MAX_RATING = 10

    def info_url(self, id):
        return f'http://www.world-art.ru/animation/animation.php?id={id}'

    def get_rating(self, id):
        soup = self._get_soup(self.info_url(id))

        rating_str = (soup.find(text='Средний балл').next_element.next_element
                      .get_text())
        rating = float(rating_str.split()[0])

        count_str = (soup.find(text='Проголосовало').next_element.next_element
                     .get_text())
        count = int(count_str.split()[0])

        return rating, count


if __name__ == '__main__':
    main(WorldArt(), '9027')
