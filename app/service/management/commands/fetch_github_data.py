from django.conf import settings
from service.api.user import GitHubUserSerializer
from service.api.repository import GitHubRepositorySerializer
from service.libs import github
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            '--num-records',
            type=int,
            default=10,
            help='Number of user records to fetch',
        )

    def handle(self, **options):
        num_records = options['num_records']
        for chunk in github.session(
            settings.GITHUB_AUTH_TOKEN
        ).fetch_data(num_records=num_records):
            users = GitHubUserSerializer(
                data=chunk, many=True, auto_instance=True
            )
            users.is_valid(raise_exception=True)
            users.save()
            users_repos = [users['repos'] for users in chunk]
            for user_repos in users_repos:
                for i, ur in enumerate(user_repos):
                    user_repos[i]['user'] = ur['owner']['id']
                    user_repos[i]['owner'] = ur['owner']['login']
                    if ur['license']:
                        user_repos[i]['license_name'] = ur['license']['name']
                user_repos = GitHubRepositorySerializer(
                    data=user_repos, many=True, auto_instance=True
                )
                user_repos.is_valid(raise_exception=True)
                user_repos.save()
        self.stdout.write('All good :)')
