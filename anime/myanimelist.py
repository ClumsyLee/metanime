from .site import main, Site


class MyAnimeList(Site):
    """myanimelist.net"""

    NAMES = {
        'en': 'MyAnimeList',
        'ja-jp': 'MyAnimeList',
        'zh-cn': 'MyAnimeList',
    }
    MIN_RATING = 1
    MAX_RATING = 10

    def info_url(self, id):
        return f'https://myanimelist.net/anime/{id}'

    def get_rating(self, id):
        soup = self._get_soup(self.info_url(id))

        rating = float(soup.find(itemprop='ratingValue').get_text())

        count_str = soup.find(itemprop='ratingCount').get_text()
        count = int(count_str.replace(',', ''))

        return rating, count


if __name__ == '__main__':
    main(MyAnimeList(), '35503')
