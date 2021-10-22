from unittest import mock
from django.test import TestCase
from django.test.utils import override_settings

from service.libs import github


class GitHubLibTest(TestCase):
    def setUp(self) -> None:
        self.users_result = [{
            "login": "mojombo",
            "id": 1,
            "node_id": "MDQ6VXNlcjE=",
            "avatar_url": "https://avatars.githubusercontent.com/u/1?v=4",
            "gravatar_id": "",
            "url": "https://api.github.com/users/mojombo",
            "html_url": "https://github.com/mojombo",
            "followers_url": "https://api.github.com/users/mojombo/followers",
            "following_url": "https://api.github.com/users/mojombo/following{/other_user}",
            "gists_url": "https://api.github.com/users/mojombo/gists{/gist_id}",
            "starred_url": "https://api.github.com/users/mojombo/starred{/owner}{/repo}",
            "subscriptions_url": "https://api.github.com/users/mojombo/subscriptions",
            "organizations_url": "https://api.github.com/users/mojombo/orgs",
            "repos_url": "https://api.github.com/users/mojombo/repos",
            "events_url": "https://api.github.com/users/mojombo/events{/privacy}",
            "received_events_url": "https://api.github.com/users/mojombo/received_events",
            "type": "User",
            "site_admin": False
        }]

        self.user_result = {
            'login': 'mojombo',
            'id': 1,
            'avatar_url': 'https://avatars.githubusercontent.com/u/1?v=4',
            'gravatar_id': '',
            'followers_url': 'https://api.github.com/users/mojombo/followers',
            'following_url': 'https://api.github.com/users/mojombo/following{/other_user}',
            'gists_url': 'https://api.github.com/users/mojombo/gists{/gist_id}',
            'starred_url': 'https://api.github.com/users/mojombo/starred{/owner}{/repo}',
            'subscriptions_url': 'https://api.github.com/users/mojombo/subscriptions',
            'organizations_url': 'https://api.github.com/users/mojombo/orgs',
            'repos_url': 'https://api.github.com/users/mojombo/repos',
            'received_events_url': 'https://api.github.com/users/mojombo/received_events',
            'type': 'User',
            'site_admin': False,
            'name': 'Tom Preston-Werner',
            'company': '@chatterbugapp, @redwoodjs, @preston-werner-ventures ',
            'blog': 'http://tom.preston-werner.com',
            'location': 'San Francisco',
            'email': 'tom@mojombo.com',
            'hireable': None,
            'bio': None,
            'twitter_username': 'mojombo',
            'public_repos': 63,
            'public_gists': 62,
            'followers': 22722,
            'following': 11,
            'updated_at': '2021-10-14T03:38:24Z'
        }

        self.repos_result = [{
            'id': 26899533,
            'name': '30daysoflaptops.github.io',
            'full_name': 'mojombo/30daysoflaptops.github.io',
            'owner': {'login': 'mojombo', 'id': 1, },
            'description': None,
            'contributors_url': 'https://api.github.com/repos/mojombo/30daysoflaptops.github.io/contributors',
            'commits_url': 'https://api.github.com/repos/mojombo/30daysoflaptops.github.io/commits{/sha}',
            'issues_url': 'https://api.github.com/repos/mojombo/30daysoflaptops.github.io/issues{/number}',
            'releases_url': 'https://api.github.com/repos/mojombo/30daysoflaptops.github.io/releases{/id}',
            'updated_at': '2021-04-03T10:15:42Z',
            'pushed_at': '2014-11-20T06:42:47Z',
            'git_url': 'git://github.com/mojombo/30daysoflaptops.github.io.git',
            'ssh_url': 'git@github.com:mojombo/30daysoflaptops.github.io.git',
            'homepage': None,
            'watchers_count': 7,
            'language': 'CSS',
            'forks_count': 2,
            'archived': False,
            'disabled': False,
            'open_issues_count': 0,
            'license': None,
            'is_template': False,
            'visibility': 'public',
            'forks': 2,
            'open_issues': 0,
            'watchers': 7,
        }, {
            'id': 17358646,
            'name': 'asteroids',
            'full_name': 'mojombo/asteroids',
            'owner': {
                    'login': 'mojombo',
                    'id': 1,
            },
            'description': 'Destroy your Atom editor, Asteroids style!',
            'contributors_url': 'https://api.github.com/repos/mojombo/asteroids/contributors',
            'commits_url': 'https://api.github.com/repos/mojombo/asteroids/commits{/sha}',
            'issues_url': 'https://api.github.com/repos/mojombo/asteroids/issues{/number}',
            'releases_url': 'https://api.github.com/repos/mojombo/asteroids/releases{/id}',
            'updated_at': '2021-04-17T13:08:46Z',
            'pushed_at': '2015-03-10T18:18:16Z',
            'git_url': 'git://github.com/mojombo/asteroids.git',
            'ssh_url': 'git@github.com:mojombo/asteroids.git',
            'homepage': None,
            'watchers_count': 93,
            'language': 'JavaScript',
            'forks_count': 13,
            'archived': False,
            'disabled': False,
            'open_issues_count': 3,
            'license': {
                'name': 'Other',
            },
            'is_template': False,
            'visibility': 'public',
            'forks': 13,
            'open_issues': 3,
            'watchers': 93,
        }]

        return super().setUp()

    @override_settings(GITHUB_AUTH_TOKEN='qwerty_token_0123')
    @mock.patch('service.libs.github.Github._fetch')
    def test_fetch_data(self, mock_fetch):
        mock_fetch.side_effect = [
            self.users_result,
            self.user_result,
            self.repos_result
        ]
        gh = github.Github(api_session=None)
        data = list(gh.fetch_data(num_records=1))
        self.assertEquals(mock_fetch.call_count, 3)
        user_ = data[0][0]
        self.assertEquals(user_['login'], self.user_result['login'])
        self.assertEquals(len(user_['repos']), len(self.repos_result))
