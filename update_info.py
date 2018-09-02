import sys
import yaml

from anime import SITES


def load_animes(filename):
    return yaml.load(open(sys.argv[1]))


def save_animes(animes, filename):
    yaml.dump(animes, open(sys.argv[1], 'w'),
              allow_unicode=True, default_flow_style=False)


def update_site_ids(anime):
    names = anime['names']
    anime.setdefault('site_ids', {})
    site_ids = anime['site_ids']

    print('Updating', names['ja-jp'])

    for site_name, site in SITES.items():
        old_site_id = site_ids.get(site_name)

        # Remove null values.
        if not old_site_id:
            site_ids.pop(site_name, None)

        print(site_name + '...')
        try:
            site_id = site.search(names)
        except Exception:
            site_id = None

        if site_id != old_site_id:
            if site_id:
                site_ids[site_name] = site_id
                print('    => ' + site.info_url(site_id))
            else:
                # Warn if becoming None.
                print('    => null?')

    print()


if __name__ == '__main__':
    filename = sys.argv[1]

    animes = load_animes(filename)
    for anime in animes.values():
        update_site_ids(anime)
    save_animes(animes, filename)
