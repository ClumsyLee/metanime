import logging
import sys

from metanime import Anime


def update_ratings(season, slug=None):
    filename = f'seasons/{season}.yml'
    animes = Anime.load(filename)

    for anime in animes:
        if slug is not None and anime.slug != slug:
            continue

        logging.info('Updating %s...', anime.slug)
        anime.update_ratings()
        Anime.dump(animes, filename)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    update_ratings(*sys.argv[1:])
