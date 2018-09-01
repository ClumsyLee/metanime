from .site import main, Site


class Douban(Site):
    """douban.com"""

    NAMES = {
        'en': 'Douban',
        'ja-jp': 'Douban',
        'zh-cn': '豆瓣',
    }
    MIN_RATING = 2
    MAX_RATING = 10

    def info_url(self, id):
        return f'https://movie.douban.com/subject/{id}'

    def get_rating(self, id):
        soup = self._get_soup(self.info_url(id))

        rating = float(soup.find(property='v:average').get_text())
        count = int(soup.find(property='v:votes').get_text())

        return rating, count


if __name__ == '__main__':
    main(Douban(), '27034594')
