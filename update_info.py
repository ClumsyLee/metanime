import logging
import sys

from metanime import Anime


def update_info(season, slug=None):
    filename = f'seasons/{season}.yml'
    animes = Anime.load(filename)

    for anime in animes:
        if anime.slug != slug:
            continue

        logging.info('Updating %s...', anime.slug)
        anime.update_info()
        Anime.dump(animes, filename)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    update_info(*sys.argv[1:])
