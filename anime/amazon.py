from .site import main, Site


class Amazon(Site):
    """amazon.com"""

    NAMES = {
        'en': 'Amazon',
        'ja-jp': 'Amazon',
        'zh-cn': 'Amazon',
    }
    MIN_RATING = 1
    MAX_RATING = 5

    def info_url(self, id):
        return f'https://www.amazon.com/dp/{id}'

    def get_rating(self, id):
        soup = self._get_soup(self.info_url(id))

        rating_str = soup.find(class_="arp-rating-out-of-text").get_text()
        rating = float(rating_str.strip().split()[0])

        count = int(soup.find(class_="totalReviewCount").get_text())

        return rating, count


if __name__ == '__main__':
    main(Amazon(), 'B078YTD3X5')
