from .site import main, Site


class Anikore(Site):
    """anikore.jp"""

    BASE_URL = 'https://www.anikore.jp'
    NAMES = {
        'en': 'Anikore',
        'ja-jp': 'Anikore',
        'zh-cn': 'Anikore',
    }
    MIN_RATING = 1
    MAX_RATING = 5
    SEARCH_LOCALES = ['ja-jp', 'en']

    def info_url(self, id):
        return f'{self.BASE_URL}/anime/{id}'

    def _get_rating(self, id):
        soup = self._get_soup(self.info_url(id))

        rating = float(
            soup.find(class_='animeDetailTopIntroduceBodyTotalReviewAllValue')
            .get_text())
        count = int(
            soup.find(class_='animeDetailTopIntroduceBodyTotalInts--review')
            .find(class_='animeDetailTopIntroduceBodyTotalIntsValue')
            .get_text())

        return rating, count

    def _search(self, name):
        soup = self._get_soup(self.BASE_URL + '/anime_title/' + name)

        href = soup.find(class_='smt_title').find('a')['href']
        id = int(href.split('/')[-2])

        return id


if __name__ == '__main__':
    main(Anikore(), {'ja-jp': '少女☆歌劇 レヴュースタァライト'})
