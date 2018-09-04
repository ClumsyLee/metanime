import json

from .site import main, Site


class AniList(Site):
    """anilist.co"""

    BASE_URL = 'https://anilist.co'
    NAMES = {
        'en': 'AniList',
        'ja-jp': 'AniList',
        'zh-cn': 'AniList',
    }
    MIN_RATING = 10
    MAX_RATING = 100

    def info_url(self, id):
        return f'{self.BASE_URL}/anime/{id}'

    def _query_media(self, query):
        return self._post_json('https://graphql.anilist.co',
                               {'query': query})['data']['Media']

    def _get_rating(self, id):
        media = self._query_media(f"""{{
            Media(id: {id}, type: ANIME) {{
                meanScore
                averageScore
                stats {{
                    scoreDistribution {{
                        score
                        amount
                    }}
                }}
            }}
        }}""")

        rating = media['averageScore']
        count = sum(entry['amount'] for entry in
                    media['stats']['scoreDistribution'])

        return rating, count

    def _search(self, name):
        search = json.dumps(name)  # Escape the name in JSON.
        media = self._query_media(f"""{{
            Media(search: {search}, type: ANIME, sort:SEARCH_MATCH) {{
                id
            }}
        }}""")

        return media['id']


if __name__ == '__main__':
    main(AniList(), {'ja-jp': '少女☆歌劇 レヴュースタァライト'})
