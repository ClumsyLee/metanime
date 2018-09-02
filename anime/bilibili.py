import re

from .site import main, Site


class Bilibili(Site):
    """bilibili.com"""

    BASE_URL = 'https://www.bilibili.com'
    NAMES = {
        'en': 'Bilibili',
        'ja-jp': 'ビリビリ',
        'zh-cn': '哔哩哔哩',
    }
    MIN_RATING = 2
    MAX_RATING = 10

    def info_url(self, id):
        return f'{self.BASE_URL}/bangumi/media/md{id}'

    def get_rating(self, id):
        soup = self._get_soup(self.info_url(id), parser='html.parser')

        rating = float(soup.find(class_='media-info-score-content').get_text())

        count_str = soup.find(class_='media-info-review-times').get_text()
        count = int(re.search(r'\d+', count_str).group())

        return rating, count

    def search(self, names):
        params = {
            'search_type': 'media_bangumi',
            'keyword': names['ja-jp']
        }
        media = self._get_json(
            'https://api.bilibili.com/x/web-interface/search/type',
            params=params)['data']['result'][0]

        return media['media_id']


if __name__ == '__main__':
    main(Bilibili(), {'ja-jp': '少女☆歌劇 レヴュースタァライト'})
