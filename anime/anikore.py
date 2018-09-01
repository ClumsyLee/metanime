from .site import main, Site


class Anikore(Site):
    """anikore.jp"""

    NAMES = {
        'en': 'Anikore',
        'ja-jp': 'Anikore',
        'zh-cn': 'Anikore',
    }
    MIN_RATING = 1
    MAX_RATING = 5

    def info_url(self, id):
        return f'https://www.anikore.jp/anime/{id}'

    def get_rating(self, id):
        soup = self._get_soup(self.info_url(id))

        rating = float(
            soup.find(class_='animeDetailTopIntroduceBodyTotalReviewAllValue')
            .get_text())
        count = int(
            soup.find(class_='animeDetailTopIntroduceBodyTotalInts--review')
            .find(class_='animeDetailTopIntroduceBodyTotalIntsValue')
            .get_text())

        return rating, count


if __name__ == '__main__':
    main(Anikore(), '11664')
