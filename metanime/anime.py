from .singleton import SITES

import logging
import yaml


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
        objs = {anime.slug: {'names': anime.names, 'site_ids': anime.site_ids}
                for anime in animes}

        with open(filename, 'w') as fp:
            return yaml.dump(objs, fp, allow_unicode=True,
                             default_flow_style=False)

    def __init__(self, slug, names=None, site_ids=None):
        if names is None:
            names = {}
        if site_ids is None:
            site_ids = {}

        self.slug = slug
        self.names = names
        self.site_ids = site_ids

    def update(self):
        self.update_names()
        self.update_site_ids()

    def update_names(self):
        names = SITES['kitsu'].get_names(self.slug)
        try:
            SITES['bangumi'].search(names, update_names=True)
        except Exception as err:
            logging.warn('Failed to update names from Bangumi: %s', err)

        names.update(self.names)
        self.names = names

    def update_site_ids(self):
        for site_name, site in SITES.items():
            # Skip static ids.
            if not site.DYNAMIC_ID and self.site_ids.get(site_name):
                continue

            logging.info('%s...', site_name)
            try:
                site_id = site.search(self.names)
                logging.info('    => %s', site.info_url(site_id))
            except Exception:
                site_id = None

            self.site_ids[site_name] = site_id
