import re

from .site import main, Site


class AnimeNewsNetwork(Site):
    """animenewsnetwork.com"""

    BASE_URL = 'https://www.animenewsnetwork.com'
    NAMES = {
        'en': 'AnimeNewsNetwork',
        'ja-jp': 'AnimeNewsNetwork',
        'zh-cn': 'AnimeNewsNetwork',
    }
    MIN_RATING = 0
    MAX_RATING = 10

    def info_url(self, id):
        return f'{self.BASE_URL}/encyclopedia/anime.php?id={id}'

    def get_rating(self, id):
        tree = self._get_xml('https://cdn.animenewsnetwork.com/encyclopedia/'
                             f'api.xml?anime={id}')
        ratings = tree.find('anime/ratings')

        rating = float(ratings.get('bayesian_score'))
        count = int(ratings.get('nb_votes'))

        return rating, count

    def search(self, names):
        soup = self._get_soup(self.BASE_URL + '/encyclopedia/search/name',
                              params={'q': names['ja-jp']})

        regex = re.compile(r'/encyclopedia/anime\.php\?id=(\d+)')
        href = soup.find('a', href=regex)['href']
        id = int(regex.search(href).group(1))

        return id


if __name__ == '__main__':
    main(AnimeNewsNetwork(), {'ja-jp': 'サクラダリセット'})
