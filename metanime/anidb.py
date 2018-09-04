from .site import main, Site


class AniDB(Site):
    """anidb.net"""

    BASE_URL = 'https://anidb.net'
    NAMES = {
        'en': 'AniDB',
        'ja-jp': 'AniDB',
        'zh-cn': 'AniDB',
    }
    MIN_RATING = 1  # See https://wiki.anidb.info/w/Votes.
    MAX_RATING = 10

    def info_url(self, id):
        return f'{self.BASE_URL}/perl-bin/animedb.pl?show=anime&aid={id}'

    def _get_rating(self, id):
        soup = self._get_soup(self.info_url(id))

        rating = float(soup.find(itemprop='ratingValue').get_text())

        count_str = soup.find(itemprop='ratingCount').get_text()
        count = int(count_str.strip('()'))

        return rating, count

    def _search(self, name):
        params = {
            'show': 'search',
            'do': 'fulltext',
            'adb.search': name,
            'entity.animetb': 1,
            'field.titles': 1,
        }
        soup = self._get_soup(self.BASE_URL + '/perl-bin/animedb.pl',
                              params=params)

        href = soup.find(class_='relid').find('a')['href']
        id = int(href.split('=')[-1])

        return id


if __name__ == '__main__':
    main(AniDB(), {'ja-jp': '少女☆歌劇 レヴュースタァライト'})
