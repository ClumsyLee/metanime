from datetime import datetime
import logging
import yaml

from .singleton import SITES


class Anime(object):
    """Anime"""

    @staticmethod
    def load(filename):
        animes = []

        with open(filename) as fp:
            for slug, attrs in yaml.load(fp).items():
                if attrs is None:
                    attrs = {}
                animes.append(Anime(slug, **attrs))

        return animes

    @staticmethod
    def dump(animes, filename):
        objs = {anime.slug: {'names': anime.names, 'sites': anime.sites}
                for anime in animes}

        with open(filename, 'w') as fp:
            return yaml.dump(objs, fp, allow_unicode=True,
                             default_flow_style=False)

    def __init__(self, slug, names=None, sites=None):
        if names is None:
            names = {}
        if sites is None:
            sites = {}

        self.slug = slug
        self.names = names
        self.sites = sites

    def update_info(self):
        self.update_names()
        self.update_ids()

    def update_names(self):
        names = SITES['kitsu'].get_names(self.slug)
        try:
            SITES['bangumi'].get_zh_cn_name(names['ja-jp'])
        except Exception as err:
            logging.warn('Failed to get zh-CN name from Bangumi: %s', err)

        names.update(self.names)  # Keep existing names.
        self.names = names

    def update_ids(self):
        for site_id, site in SITES.items():
            # Skip existing sites unless they use dynamic ids.
            # Notice that we'll skip even self.sites[site_id] is None.
            # This ensures that there's a way to override false matches.
            if not site.DYNAMIC_ID and site_id in self.sites:
                continue

            logging.info('%s...', site_id)
            id = site.search(self.names)

            if id is not None:
                if ((self.sites.get(site_id) and
                     self.sites[site_id].get('id') == id)):
                    continue  # The ID doesn't change.

                self.sites[site_id] = {'id': id}
                logging.info('    => %s', site.info_url(id))

    def update_ratings(self):
        for site_id, info in self.sites.items():
            if info is None:
                continue

            logging.info('%s...', site_id)
            rating, count = SITES[site_id].get_rating(info['id'])

            if rating is not None:
                info['rating'] = rating

                if count is None:
                    info.pop('rating_count', None)
                    logging.info('    => %f', rating)
                else:
                    info['rating_count'] = count
                    logging.info('    => %g (%d)', rating, count)

                info['updated_at'] = iso8601_now()


def iso8601_now():
    return datetime.utcnow().replace(microsecond=0).isoformat() + 'Z'
