import logging
import sys

from metanime import Anime, Renderer


def render(season):
    animes = Anime.load(f'seasons/{season}.yml')
    renderer = Renderer('views', 'docs')

    for anime in animes:
        renderer.render_anime(anime)
    renderer.render_season(season, animes)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    render(sys.argv[1])
