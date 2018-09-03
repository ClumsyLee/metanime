from .singleton import SITES

import logging
import yaml


def without_none(d):
    if d is None:
        return {}
    else:
        return {key: value for key, value in d.items() if value is None}


class Anime(object):
    """Anime"""

    @staticmethod
    def load(filename):
        animes = []

        with open(filename) as fp:
            for slug, attrs in yaml.load(fp).items():
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
        self.slug = slug
        self.names = without_none(names)
        self.site_ids = without_none(site_ids)

    def update(self):
        self.update_names()
        self.update_site_ids()

    def update_names(self):
        names = SITES['kitsu'].get_names(self.slug)
        SITES['douban'].search(names, update_names=True)

        self.names = names

    def update_site_ids(self):
        for site_name, site in SITES.items():
            old_site_id = self.site_ids.get(site_name)

            logging.info('%s...', site_name)
            try:
                site_id = site.search(self.names)
            except Exception:
                site_id = None

            if site_id != old_site_id:
                if site_id is None:
                    # Warn if becoming None.
                    logging.warn('    => null?')
                else:
                    self.site_ids[site_name] = site_id
                    logging.info('    => %s', site.info_url(site_id))
