from statistics import mean
from jinja2 import Environment, FileSystemLoader

from .singleton import SITES


class Renderer(object):
    """Renderer"""

    ANIME_TEMPLATE = 'anime.html'

    def __init__(self, animes, input_dir, output_dir):
        self.animes = animes
        self.input_dir = input_dir
        self.output_dir = output_dir

        self.env = Environment(loader=FileSystemLoader(input_dir))
        self.anime_template = self.env.get_template(self.ANIME_TEMPLATE)

    def render_anime(self, anime):
        rows = []
        others = []

        for site_id, info in anime.sites.items():
            if info is None:
                continue

            site = SITES[site_id]
            url = site.info_url(info['id'])

            rating = info.get('rating')
            count = info.get('rating_count')
            if rating is not None:
                caption = f'{round(rating, 2)} ({count})'
                if count >= 10:
                    rating = site.unify_rating(rating)
                    rows.append((site_id, url, caption, rating))
                else:
                    others.append((site_id, url, caption, ''))
            else:
                caption = ''
                rating = ''
                others.append((site_id, url, caption, rating))

        average = mean(row[-1] for row in rows)
        rows.sort(key=lambda row: row[-1], reverse=True)
        others.sort(key=lambda row: row[0])

        params = {
            'name': anime.names.get('zh-cn', anime.names['ja-jp']),
            'subtitle': anime.names['ja-jp'],
            'average_rating': average,
            'highers': [row for row in rows if average + 5 <= row[-1]],
            'highs': [row for row in rows if average <= row[-1] < average + 5],
            'lows': [row for row in rows if average - 5 < row[-1] < average],
            'lowers': [row for row in rows if row[-1] <= average - 5],
            'others': others,
            'i18n': {
                'navbar.current_season': '当季番剧',
                'navbar.about': '关于',
                'navbar.about': '关于',
                'site_name.average': '平均',
            },
        }

        for site_id, site in SITES.items():
            params['i18n']['site_name.' + site_id] = site.NAMES['zh-cn']

        with open(f'{self.output_dir}/{anime.slug}.html', 'w') as fp:
            fp.write(self.anime_template.render(params))
