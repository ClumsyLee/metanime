from .site import main, Site


class AniList(Site):
    """anilist.co"""

    NAMES = {
        'en': 'AniList',
        'ja-jp': 'AniList',
        'zh-cn': 'AniList',
    }
    MIN_RATING = 10
    MAX_RATING = 100

    def info_url(self, id):
        return f'https://anilist.co/anime/{id}'

    def _get_info(self, id):
        query = """{
            Media(id: 98658, type: ANIME) {
                meanScore
                averageScore
                stats {
                    scoreDistribution {
                        score
                        amount
                    }
                }
            }
        }"""
        return self._post_json('https://graphql.anilist.co',
                               {'query': query})['data']['Media']

    def get_rating(self, id):
        info = self._get_info(id)

        rating = info['averageScore']
        count = sum(entry['amount'] for entry in
                    info['stats']['scoreDistribution'])

        return rating, count


if __name__ == '__main__':
    main(AniList(), 'shoujo-kageki-revue-starlight')
