from datetime import datetime, timezone
from django.test import TestCase

from service import models


class RepositoryTest(TestCase):
    def setUp(self) -> None:
        self.user_ = [{
            'id': 1,
            'login': 'mojombo',
            'name': 'Tom Preston-Werner',
            'company': '@chatterbugapp, @redwoodjs, @preston-werner-ventures',
            'blog': 'http://tom.preston-werner.com',
            'location': 'San Francisco',
            'email': 'tom@mojombo.com',
            'bio': None,
            'public_repos': 63,
            'twitter_username': 'mojombo',
            'updated_at': '2021-10-14T03:38:24Z',
            'repos': [{
                "uid": "dcbf2bbc-26e8-43f4-aab1-dda61be8d3df",
                "id": 26899533,
                "owner": "mojombo",
                "name": "30daysoflaptops.github.io",
                "full_name": "mojombo/30daysoflaptops.github.io",
                "description": None,
                "homepage": None,
                "visibility": "public",
                "watchers_count": 7,
                "forks_count": 2,
                "open_issues_count": 0,
                "archived": None,
                "is_template": False,
                "language": "CSS",
                "license_name": None,
                "disabled": False,
                "pushed_at": "2014-11-20T06:42:47Z",
                "updated_at": "2021-04-03T10:15:42Z",
                "user": 1
            }, {
                "uid": "db4d5b52-c41e-4d2d-9e8e-600714a427ab",
                "id": 17358646,
                "owner": "mojombo",
                "name": "asteroids",
                "full_name": "mojombo/asteroids",
                "description": "Destroy your Atom editor, Asteroids style!",
                "homepage": None,
                "visibility": "public",
                "watchers_count": 93,
                "forks_count": 13,
                "open_issues_count": 3,
                "archived": False,
                "is_template": False,
                "language": "JavaScript",
                "license_name": "Other",
                "disabled": False,
                "pushed_at": "2015-03-10T18:18:16Z",
                "updated_at": "2021-04-17T13:08:46Z",
                "user": 1
            }]
        }]
        return super().setUp()

    def test_viewset_list(self):
        res = self.client.get('/api/github/repository/')
        expected = {'count': 0, 'next': None, 'previous': None, 'results': []}
        self.assertEquals(expected, res.json())

    def test_viewset_retrieve(self):
        user_ = models.GitHubUser(
            id=1, login='mojombo', public_repos=1,
            updated_at=datetime.now(timezone.utc)
        )
        user_.save()
        repo_ = models.GitHubRepository(
            id=1, name='mojombo/teste', updated_at=datetime.now(timezone.utc),
            open_issues_count=10, watchers_count=10, forks_count=10,
            user_id=1
        )
        repo_.save()
        res = self.client.get(
            f'/api/github/repository/{repo_.uid}/'
        ).json()
        self.assertEquals(res['name'], 'mojombo/teste')
        self.assertEquals(res['user'], 1)
