import re

from .site import main, Site


class Bilibili(Site):
    """bilibili.com"""

    NAMES = {
        'en': 'Bilibili',
        'ja-jp': 'ビリビリ',
        'zh-cn': '哔哩哔哩',
    }
    MIN_RATING = 2
    MAX_RATING = 10

    def info_url(self, id):
        return f'https://www.bilibili.com/bangumi/media/{id}'

    def get_rating(self, id):
        soup = self._get_soup(self.info_url(id), parser='html.parser')

        rating = float(soup.find(class_='media-info-score-content').get_text())

        count_str = soup.find(class_='media-info-review-times').get_text()
        count = int(re.search(r'\d+', count_str).group())

        return rating, count


if __name__ == '__main__':
    main(Bilibili(), 'md102892')
