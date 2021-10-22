from copy import deepcopy
from datetime import datetime, timezone
from unittest import mock
from django.test import TestCase
from rest_framework.exceptions import ValidationError

from service.api import user
from service import models


class UserTest(TestCase):
    def setUp(self) -> None:
        self.maxDiff = None
        self.base_data = [{
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
            'updated_at': '2021-10-14T03:38:24Z'
        }, {
            'id': 2,
            'login': 'defunkt',
            'name': 'Chris Wanstrath',
            'company': None,
            'blog': 'http://chriswanstrath.com/',
            'location': None,
            'email': None,
            'bio': 'hamburguer',
            'public_repos': 107,
            'twitter_username': None,
            'updated_at': '2021-07-29T11:10:23Z'
        }]
        return super().setUp()

    def test_viewset_list(self):
        res = self.client.get('/api/github/user/')
        expected = {'count': 0, 'next': None, 'previous': None, 'results': []}
        self.assertEquals(expected, res.json())

    def test_viewset_retrieve(self):
        user_ = models.GitHubUser(
            id=1, login='mojombo', public_repos=1,
            updated_at=datetime.now(timezone.utc)
        )
        user_.save()
        res = self.client.get(
            f'/api/github/user/{user_.uid}/'
        ).json()
        self.assertEquals(res['login'], 'mojombo')

    def test_serializer_invalid_data(self):
        data = {'invalid': 'data'}
        serializer = user.GitHubUserSerializer(data=data)
        with self.assertRaises(ValidationError) as context:
            serializer.is_valid(raise_exception=True)
        self.assertEquals(
            str(context.exception),
            (
                "{'id': [ErrorDetail(string='This field is required.', "
                "code='required')], 'login': [ErrorDetail(string='This field "
                "is required.', code='required')], 'name': "
                "[ErrorDetail(string='This field is required.', "
                "code='required')], 'public_repos': "
                "[ErrorDetail(string='This field is required.', "
                "code='required')], 'updated_at': [ErrorDetail(string='This "
                "field is required.', code='required')]}"
            )
        )

    def test_serializer_many_invalid_data(self):
        data = [{'id': '1'}, {'invalid': 'data'}]
        with self.assertRaises(ValidationError) as context:
            user.GitHubUserSerializer(data=data, many=True)
        self.assertEquals(
            str(context.exception),
            "{'id': ErrorDetail(string='id field is required for entire "
            "dataset', code='invalid')}"
        )

    @mock.patch('service.libs.github.session')
    def test_serializer_many_missing_required_data(self, session):
        data = [{'id': '1'}]
        serializer = user.GitHubUserSerializer(data=data, many=True)
        with self.assertRaises(ValidationError) as context:
            serializer.is_valid(raise_exception=True)
        self.assertEquals(
            str(context.exception),
            (
                "[{'login': [ErrorDetail(string='This field "
                "is required.', code='required')], 'name': "
                "[ErrorDetail(string='This field is required.', "
                "code='required')], 'public_repos': "
                "[ErrorDetail(string='This field is required.', "
                "code='required')], 'updated_at': [ErrorDetail(string='This "
                "field is required.', code='required')]}]"
            )
        )

    @mock.patch('service.libs.github.session')
    def test_serializer_missing_required_data(self, session):
        data = {'id': '1'}
        serializer = user.GitHubUserSerializer(data=data)
        with self.assertRaises(ValidationError) as context:
            serializer.is_valid(raise_exception=True)
        self.assertEquals(
            str(context.exception),
            (
                "{'login': [ErrorDetail(string='This field "
                "is required.', code='required')], 'name': "
                "[ErrorDetail(string='This field is required.', "
                "code='required')], 'public_repos': "
                "[ErrorDetail(string='This field is required.', "
                "code='required')], 'updated_at': [ErrorDetail(string='This "
                "field is required.', code='required')]}"
            )
        )

    @mock.patch('service.libs.github.session')
    def test_serializer(self, session):
        data = self.base_data[0]
        serializer = user.GitHubUserSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        self.assertEquals(models.GitHubUser.objects.get(id=1).login, 'mojombo')

    @mock.patch('service.libs.github.session')
    def test_serializer_many(self, session):
        serializer = user.GitHubUserSerializer(data=self.base_data, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        self.assertEquals(models.GitHubUser.objects.get(id=1).login, 'mojombo')
        self.assertEquals(models.GitHubUser.objects.count(), 2)

    @mock.patch('service.libs.github.session')
    def test_serializer_many_update(self, session):
        data = deepcopy(self.base_data)
        serializer = user.GitHubUserSerializer(data=data, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        self.assertEquals(models.GitHubUser.objects.get(id=1).login, 'mojombo')
        self.assertEquals(models.GitHubUser.objects.count(), 2)

        data[0]['bio'] = 'test many update'
        serializer = user.GitHubUserSerializer(data=data, many=True,
                                               auto_instance=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        self.assertEquals(
            models.GitHubUser.objects.get(id=1).bio,
            'test many update'
        )
