import logging
import sys

from metanime import Anime


logging.basicConfig(level=logging.INFO)


if __name__ == '__main__':
    filename = sys.argv[1]
    animes = Anime.load(filename)

    for anime in animes:
        anime.update()

    Anime.dump(animes, filename)
