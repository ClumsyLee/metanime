import logging
import sys

from metanime import Anime


def update_info(filename):
    animes = Anime.load(filename)
    for anime in animes:
        logging.info('Updating %s...', anime.slug)
        anime.update()
        Anime.dump(animes, filename)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    update_info(f'seasons/{sys.argv[1]}/info.yml')
