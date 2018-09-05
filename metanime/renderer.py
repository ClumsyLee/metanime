from statistics import mean
from jinja2 import Environment, FileSystemLoader

from .singleton import SITES


I18NS = {
    'zh-cn': {
        'navbar.current_season': '当季番剧',
        'navbar.about': '关于',
        'row.average': '平均',
    }
}


class Row(object):
    """Row"""

    def __init__(self, name, url, caption='', rating=None,
                 link_class='metanime'):
        self.name = name
        self.url = url
        self.caption = caption
        self.rating = rating
        self.link_class = link_class


class Renderer(object):
    """Renderer"""

    ANIME_TEMPLATE = 'anime.html'

    def __init__(self, input_dir, output_dir):
        self.input_dir = input_dir
        self.output_dir = output_dir

        self.env = Environment(loader=FileSystemLoader(input_dir))
        self.anime_template = self.env.get_template(self.ANIME_TEMPLATE)

    def render_anime(self, anime):
        rows = []
        other_rows = []

        for site_id, info in anime.sites.items():
            if info is None or info.get('id') is None:
                continue

            site = SITES[site_id]
            name = site.NAMES['zh-cn']
            url = site.info_url(info['id'])

            rating = info.get('rating')
            count = info.get('rating_count')

            if rating is None:
                other_rows.append(Row(name, url, link_class=site_id))
            else:
                caption = str(round(rating, 2))
                if count is not None:
                    caption += f' ({count})'

                if count is not None and count >= 10:
                    unified_rating = site.unify_rating(rating)
                    rows.append(Row(name, url, caption=caption,
                                    rating=unified_rating,
                                    link_class=site_id))
                else:
                    other_rows.append(Row(name, url, caption=caption,
                                          link_class=site_id))

        average = mean(row.rating for row in rows) if rows else None
        rows.sort(key=lambda row: row.rating, reverse=True)
        other_rows.sort(key=lambda row: row.name)

        path = '/' + anime.slug

        name = anime.names.get('zh-cn')
        subtitle = anime.names['ja-jp']
        if name is None:
            name = subtitle
            subtitle = None

        params = {
            'path': path,
            'name': name,
            'subtitle': subtitle,
            'average_rating': average,
            'higher_rows': [row for row in rows
                            if average + 5 <= row.rating],
            'high_rows': [row for row in rows
                          if average <= row.rating < average + 5],
            'low_rows': [row for row in rows
                         if average - 5 < row.rating < average],
            'lowers_rows': [row for row in rows
                            if row.rating <= average - 5],
            'other_rows': other_rows,
            'i18n': I18NS['zh-cn'],
        }

        with open(self.output_dir + path + '.html', 'w') as fp:
            fp.write(self.anime_template.render(params))
