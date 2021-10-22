from io import StringIO

from unittest import mock

from django.core.management import call_command

from django.test import TestCase
from django.test.utils import override_settings


class FetchGithubDataCommandTestCase(TestCase):

    def setUp(self) -> None:
        self.out = StringIO()
        return super().setUp()

    def test_no_auth_token(self):
        with self.assertRaises(RuntimeError) as context:
            call_command('fetch_github_data')

        self.assertEquals(
            str(context.exception),
            'Unable to create api session, setup GITHUB_AUTH_TOKEN or pass auth_token'
        )

    @override_settings(GITHUB_AUTH_TOKEN='qwerty_token_0123')
    def test_bad_credentials(self):
        with self.assertRaises(RuntimeError) as context:
            call_command('fetch_github_data')

        self.assertEquals(
            str(context.exception),
            '401: Bad credentials (https://docs.github.com/rest)'
        )

    @override_settings(GITHUB_AUTH_TOKEN='qwerty_token_0123')
    @mock.patch('service.libs.github.session')
    def test_empty_dataset(self, session):
        github = mock.MagicMock()
        session.return_value = github

        github.fetch_data.return_value = [[]]
        call_command('fetch_github_data', stdout=self.out)

        self.assertIn('All good :)\n', self.out.getvalue())
        github.fetch_data.assert_called_once()

    @override_settings(GITHUB_AUTH_TOKEN='querty_token_0123')
    @mock.patch('service.libs.github.session')
    def test_common_workflow(self, session):
        github = mock.MagicMock()
        session.return_value = github

        github.fetch_data.return_value = [[{
            'login': 'mojombo', 'id': 1,
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
            'type': 'User', 'site_admin': False, 'name': 'Tom Preston-Werner',
            'company': '@chatterbugapp, @redwoodjs, @preston-werner-ventures ',
            'blog': 'http://tom.preston-werner.com', 'location': 'San Francisco',
            'email': 'tom@mojombo.com', 'hireable': None, 'bio': None, 'twitter_username':
            'mojombo', 'public_repos': 63, 'public_gists': 62, 'followers': 22722,
            'following': 11, 'updated_at': '2021-10-14T03:38:24Z',
            'repos': [{
                'id': 26899533, 'name': '30daysoflaptops.github.io',
                'full_name': 'mojombo/30daysoflaptops.github.io',
                'owner': {'login': 'mojombo', 'id': 1},
                'description': None,
                'contributors_url': 'https://api.github.com/repos/mojombo/30daysoflaptops.github.io/contributors',
                'commits_url': 'https://api.github.com/repos/mojombo/30daysoflaptops.github.io/commits{/sha}',
                'issues_url': 'https://api.github.com/repos/mojombo/30daysoflaptops.github.io/issues{/number}',
                'releases_url': 'https://api.github.com/repos/mojombo/30daysoflaptops.github.io/releases{/id}',
                'updated_at': '2021-04-03T10:15:42Z',
                'pushed_at': '2014-11-20T06:42:47Z',
                'git_url': 'git://github.com/mojombo/30daysoflaptops.github.io.git',
                'ssh_url': 'git@github.com:mojombo/30daysoflaptops.github.io.git',
                'homepage': None, 'watchers_count': 7, 'language': 'CSS', 'forks_count': 2,
                'archived': False, 'disabled': False, 'open_issues_count': 0,
                'license': None, 'is_template': False, 'visibility': 'public',
                'forks': 2, 'open_issues': 0, 'watchers': 7
            }, {
                'id': 17358646, 'name': 'asteroids',
                'full_name': 'mojombo/asteroids',
                'owner': {'login': 'mojombo', 'id': 1},
                'description': 'Destroy your Atom editor, Asteroids style!',
                'contributors_url': 'https://api.github.com/repos/mojombo/asteroids/contributors',
                'commits_url': 'https://api.github.com/repos/mojombo/asteroids/commits{/sha}',
                'issues_url': 'https://api.github.com/repos/mojombo/asteroids/issues{/number}',
                'releases_url': 'https://api.github.com/repos/mojombo/asteroids/releases{/id}',
                'updated_at': '2021-04-17T13:08:46Z', 'pushed_at': '2015-03-10T18:18:16Z',
                'git_url': 'git://github.com/mojombo/asteroids.git',
                'ssh_url': 'git@github.com:mojombo/asteroids.git', 'homepage': None,
                'watchers_count': 93, 'language': 'JavaScript', 'forks_count': 13,
                'archived': False, 'disabled': False, 'open_issues_count': 3,
                'license': {'name': 'Other'}, 'is_template': False,
                'visibility': 'public', 'forks': 13, 'open_issues': 3,
                'watchers': 93
            }]
        }]]

        call_command('fetch_github_data', stdout=self.out)

        self.assertIn('All good :)', self.out.getvalue())
        github.fetch_data.assert_called_once()
