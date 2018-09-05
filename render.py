import logging
import sys

from metanime import Anime, Renderer


def render(filename, input_dir, output_dir):
    animes = Anime.load(filename)
    renderer = Renderer(input_dir, output_dir)

    for anime in animes:
        renderer.render_anime(anime)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    render(f'seasons/{sys.argv[1]}.yml', 'views', 'docs')
