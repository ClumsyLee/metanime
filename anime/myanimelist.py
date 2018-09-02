from .site import main, Site


class MyAnimeList(Site):
    """myanimelist.net"""

    BASE_URL = 'https://myanimelist.net'
    NAMES = {
        'en': 'MyAnimeList',
        'ja-jp': 'MyAnimeList',
        'zh-cn': 'MyAnimeList',
    }
    MIN_RATING = 1
    MAX_RATING = 10

    def info_url(self, id):
        return f'{self.BASE_URL}/anime/{id}'

    def get_rating(self, id):
        soup = self._get_soup(self.info_url(id))

        rating = float(soup.find(itemprop='ratingValue').get_text())

        count_str = soup.find(itemprop='ratingCount').get_text()
        count = int(count_str.replace(',', ''))

        return rating, count

    def search(self, names):
        params = {
            'type': 'anime',
            'keyword': names['ja-jp'],
        }
        media = self._get_json(self.BASE_URL + '/search/prefix.json',
                               params=params)['categories'][0]['items'][0]

        return media['id']


if __name__ == '__main__':
    main(MyAnimeList(), {'ja-jp': '少女☆歌劇 レヴュースタァライト'})
