from .site import main, Site


class AniDB(Site):
    """anidb.net"""

    NAMES = {
        'en': 'AniDB',
        'ja-jp': 'AniDB',
        'zh-cn': 'AniDB',
    }
    MIN_RATING = 1  # See https://wiki.anidb.info/w/Votes.
    MAX_RATING = 10

    def info_url(self, id):
        return f'https://anidb.net/perl-bin/animedb.pl?show=anime&aid={id}'

    def get_rating(self, id):
        soup = self._get_soup(self.info_url(id))

        rating = float(soup.find(itemprop='ratingValue').get_text())

        count_str = soup.find(itemprop='ratingCount').get_text()
        count = int(count_str.strip('()'))

        return rating, count


if __name__ == '__main__':
    main(AniDB(), '13152')
