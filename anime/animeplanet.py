from .site import main, Site


class AnimePlanet(Site):
    """anime-planet.com"""

    NAMES = {
        'en': 'AnimePlanet',
        'ja-jp': 'AnimePlanet',
        'zh-cn': 'AnimePlanet',
    }
    MIN_RATING = 1
    MAX_RATING = 10

    def info_url(self, id):
        return f'https://www.anime-planet.com/anime/{id}'

    def get_rating(self, id):
        soup = self._get_soup(self.info_url(id))

        rating = float(soup.find(itemprop='ratingValue')['content'])
        count = int(soup.find(itemprop='ratingCount')['content'])

        return rating, count


if __name__ == '__main__':
    main(AnimePlanet(), 'shoujo-kageki-revue-starlight')
