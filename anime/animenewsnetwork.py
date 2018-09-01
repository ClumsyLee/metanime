from .site import main, Site


class AnimeNewsNetwork(Site):
    """animenewsnetwork.com"""

    NAMES = {
        'en': 'AnimeNewsNetwork',
        'ja-jp': 'AnimeNewsNetwork',
        'zh-cn': 'AnimeNewsNetwork',
    }
    MIN_RATING = 0
    MAX_RATING = 10

    def info_url(self, id):
        return ('https://www.animenewsnetwork.com/encyclopedia/anime.php?'
                f'id={id}')

    def get_rating(self, id):
        soup = self._get_soup(self.info_url(id))

        rating_str = soup.find(text='Bayesian estimate:').next_element
        rating = float(rating_str.strip().split()[0])

        count_str = (soup.find(text='User Ratings:').next_element.next_element
                     .get_text())
        count = int(count_str.strip().split()[0])

        return rating, count


if __name__ == '__main__':
    main(AnimeNewsNetwork(), '18950')
