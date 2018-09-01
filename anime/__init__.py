from .amazon import Amazon
from .anidb import AniDB
from .anilist import AniList
from .bangumi import Bangumi
from .bilibili import Bilibili
from .crunchyroll import Crunchyroll
from .douban import Douban
from .imdb import IMDB
from .kitsu import Kitsu
from .myanimelist import MyAnimeList
from .reddit import Reddit


SITES = {
    'amazon': Amazon(),
    'anidb': AniDB(),
    'anilist': AniList(),
    'bangumi': Bangumi(),
    'bilibili': Bilibili(),
    'crunchyroll': Crunchyroll(),
    'douban': Douban(),
    'imdb': IMDB(),
    'kitsu': Kitsu(),
    'myanimelist': MyAnimeList(),
    'reddit': Reddit(),
}
