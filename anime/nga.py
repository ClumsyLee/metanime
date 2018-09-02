import os

from .site import main, Site


class NGA(Site):
    """ngacn.cc"""

    BASE_URL = 'https://bbs.ngacn.cc'
    NAMES = {
        'en': 'NGA',
        'ja-jp': 'NGA',
        'zh-cn': 'NGA',
    }
    MIN_RATING = 1
    MAX_RATING = 10

    def __init__(self, uid=None, cid=None):
        super().__init__()

        if uid is None:
            uid = os.getenv('NGA_UID')
        if cid is None:
            cid = os.getenv('NGA_CID')
        if uid is None or cid is None:
            raise ValueError('uid and cid must be provided')

        self.session.headers['Cookie'] = (
            f'ngaPassportUid={uid};'
            f'ngaPassportCid={cid};'
        )

    def info_url(self, id):
        return f'{self.BASE_URL}/read.php?tid={id}'

    def get_rating(self, id):
        soup = self._get_soup(self.info_url(id))
        vote_script = soup.find(id='votec0').next_sibling.string
        vote_parts = vote_script.split('~')[-1].split(',')

        count = int(vote_parts[0])
        rating = int(vote_parts[1]) / count

        return rating, count

    def search(self, names):
        params = {
            'key': names['ja-jp'],
            'fid': 572,
            'content': 1,
        }
        soup = self._get_soup(self.BASE_URL + '/thread.php', params=params)

        href = soup.find('a', class_='topic')['href']
        id = href.split('=')[-1]

        return id


if __name__ == '__main__':
    main(NGA(), {'ja-jp': 'サクラダリセット'})
