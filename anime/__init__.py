from .amazon import Amazon
from .anidb import AniDB
from .anikore import Anikore
from .anilist import AniList
from .animenewsnetwork import AnimeNewsNetwork
from .bangumi import Bangumi
from .bilibili import Bilibili
from .crunchyroll import Crunchyroll
from .douban import Douban
from .imdb import IMDB
from .kitsu import Kitsu
from .myanimelist import MyAnimeList
from .reddit import Reddit
from .saraba1st import Saraba1st


SITES = {
    'amazon': Amazon(),
    'anidb': AniDB(),
    'anikore': Anikore(),
    'anilist': AniList(),
    'animenewsnetwork': AnimeNewsNetwork(),
    'bangumi': Bangumi(),
    'bilibili': Bilibili(),
    'crunchyroll': Crunchyroll(),
    'douban': Douban(),
    'imdb': IMDB(),
    'kitsu': Kitsu(),
    'myanimelist': MyAnimeList(),
    'reddit': Reddit(),
    'saraba1st': Saraba1st(),
}
