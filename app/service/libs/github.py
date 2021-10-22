
import os
import requests

GITHUB_USER_TYPE = 'User'
GITHUB_DEFAULT_PAGE_SIZE = 30
GITHUB_MAX_PAGE_SIZE = 100


def session(auth_token=None):
    auth_token = auth_token or os.getenv('GITHUB_AUTH_TOKEN', None)
    if not auth_token:
        raise RuntimeError('Unable to create api session, setup '
                           'GITHUB_AUTH_TOKEN or pass auth_token')
    session = requests.Session()
    session.headers.update({
        'Accept': 'application/vnd.github.v3+json',
        'Authorization': f'token {auth_token}',
    })

    return Github.create(session)


class Github:
    def __init__(self, api_session: requests.Session):
        self.api_session = api_session

    @classmethod
    def create(cls, api_session):
        return cls(api_session)

    def _fetch(self, url):
        res = self.api_session.get(url)
        if res.status_code != 200:
            error = res.json()
            raise RuntimeError(f'{res.status_code}: {error["message"]} '
                               f'({error["documentation_url"]})')
        return res.json()

    def fetch_data(self, num_records=GITHUB_DEFAULT_PAGE_SIZE):
        since = 0
        per_page = GITHUB_MAX_PAGE_SIZE

        while num_records > 0:
            if num_records < GITHUB_MAX_PAGE_SIZE:
                per_page = num_records
            users = self._fetch(f'https://api.github.com/users'
                                f'?since={since}&per_page={per_page}')
            users = [u for u in users if u['type'] == GITHUB_USER_TYPE]
            for i, user in enumerate(users):
                users[i] = self._fetch(user['url'])
                users[i]['repos'] = self._fetch(user['repos_url'])
            yield users
            num_records -= per_page
            since += per_page
