import logging
import sys

from metanime import Anime


def update_info(filename):
    animes = Anime.load(filename)
    for anime in animes:
        anime.update()
    Anime.dump(animes, filename)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    update_info(sys.argv[1])
