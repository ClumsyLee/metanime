from .site import main, Site


class AnimePlanet(Site):
    """anime-planet.com"""

    BASE_URL = 'https://www.anime-planet.com'
    NAMES = {
        'en': 'AnimePlanet',
        'ja-jp': 'AnimePlanet',
        'zh-cn': 'AnimePlanet',
    }
    MIN_RATING = 1
    MAX_RATING = 10
    SEARCH_LOCALES = ['ja-jp', 'en-jp']

    def info_url(self, id):
        return f'{self.BASE_URL}/anime/{id}'

    def _get_rating(self, id):
        soup = self._get_soup(self.info_url(id))

        rating = float(soup.find(itemprop='ratingValue')['content'])
        count = int(soup.find(itemprop='ratingCount')['content'])

        return rating, count

    def _search(self, name):
        params = {
            'name': name,
            'sort': 'status_2',
            'order': 'desc',
        }
        soup = self._get_soup(self.BASE_URL + '/anime/all', params=params)
        og_url = soup.find('meta', property='og:url')

        # Handle exact match
        if og_url is not None:
            href = og_url['content']
        else:
            href = soup.find(class_='cardDeck').find('a')['href']
        id = href.split('/')[-1]

        return id


if __name__ == '__main__':
    main(AnimePlanet(), {'ja-jp': '少女☆歌劇 レヴュースタァライト'})
