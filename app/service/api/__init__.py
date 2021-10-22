from django.apps import AppConfig
from django.contrib import admin


class ServiceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'service'

    def ready(self):
        from service.models import GitHubUser, GitHubRepository
        from service.api.user import GitHubUserAdmin
        from service.api.repository import GithubRepositoryAdmin

        admin.site.register(GitHubUser, GitHubUserAdmin)
        admin.site.register(GitHubRepository, GithubRepositoryAdmin)
