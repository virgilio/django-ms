import uuid

from django.db import models


class GitHubUser(models.Model):
    uid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    id = models.PositiveBigIntegerField(unique=True)  # 1
    login = models.CharField(max_length=127, unique=True)  # mojombo
    avatar_url = models.URLField()  # https://avatars.git...content.com/u/1?v=4
    name = models.CharField(max_length=255, null=True)  # Tom Preston-Werner
    company = models.CharField(max_length=255, null=True)  # @chatterbug
    blog = models.CharField(max_length=255, null=True, blank=True)
    location = models.CharField(max_length=255, null=True)  # San Francisco
    email = models.EmailField(null=True, blank=True)  # None
    bio = models.TextField(null=True, blank=True)  # None
    public_repos = models.IntegerField()  # 63
    twitter_username = models.CharField(max_length=127, null=True)  # mojombo
    updated_at = models.DateTimeField()  # 2021-10-14T03:38:24Z

    @property
    def avatar_url(self):
        return f'https://avatars.githubusercontent.com/u/{self.github_id}?v=4'

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'service'
        verbose_name = 'Github User'
        verbose_name_plural = 'Github Users'


class GitHubRepository(models.Model):
    uid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    id = models.PositiveBigIntegerField(unique=True)  # 1
    owner = models.CharField(max_length=127)  # mojombo
    user = models.ForeignKey(
        GitHubUser, on_delete=models.CASCADE,
        to_field='id', related_name='repos'
    )
    name = models.CharField(max_length=127)  # grit
    full_name = models.CharField(max_length=255)  # mojombo/grit
    description = models.TextField(null=True)  # **Grit is longer (...) Ruby.
    homepage = models.CharField(max_length=255, null=True, blank=True)
    visibility = models.CharField(max_length=31)  # public
    watchers_count = models.IntegerField()  # 1934
    forks_count = models.IntegerField()  # 537
    open_issues_count = models.IntegerField()  # 27
    archived = models.BooleanField(default=False)  # False
    is_template = models.BooleanField(default=False)  # False
    language = models.CharField(max_length=127, null=True)  # Ruby
    license_name = models.CharField(max_length=127, null=True)  # MIT License
    disabled = models.BooleanField(default=False)  # False
    pushed_at = models.DateTimeField(null=True)  # 2020-10-01T03:55:32Z
    updated_at = models.DateTimeField(null=True)  # 2021-10-22T14:49:27Z

    @property
    def issues_url(self):  # https://api.github.com/repos/mojombo/grit/issues
        return f'https://api.github.com/repos/{self.owner}/{self.name}/issues'

    @property
    def releases_url(self):  # https://api.gh.com/repos/mojombo/grit/releases
        return (f'https://api.github.com/repos/'
                f'{self.owner}/{self.name}/releases')

    @property
    def contributors_url(self):  # api.gh.com/repos/mojombo/grit/contributors
        return (f'https://api.github.com/repos/'
                f'{self.owner}/{self.name}/contributors')

    @property
    def git_url(self):  # git://github.com/mojombo/grit.git
        return f'git://github.com/{self.owner}/{self.name}.git'

    @property
    def ssh_url(self):  # git@github.com:mojombo/grit.git
        return f'git@github.com:{self.owner}/{self.name}.git'

    def __str__(self):
        return f'{self.full_name} - {self.description}'

    class Meta:
        app_label = 'service'
        verbose_name = 'Github Repository'
        verbose_name_plural = 'Github Repositories'
