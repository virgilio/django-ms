# Generated by Django 3.2.8 on 2022-06-24 14:19

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GitHubUser',
            fields=[
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('id', models.PositiveBigIntegerField(unique=True)),
                ('login', models.CharField(max_length=127, unique=True)),
                ('name', models.CharField(max_length=255, null=True)),
                ('company', models.CharField(max_length=255, null=True)),
                ('blog', models.CharField(blank=True, max_length=255, null=True)),
                ('location', models.CharField(max_length=255, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('bio', models.TextField(blank=True, null=True)),
                ('public_repos', models.IntegerField()),
                ('twitter_username', models.CharField(max_length=127, null=True)),
                ('updated_at', models.DateTimeField()),
            ],
            options={
                'verbose_name': 'Github User',
                'verbose_name_plural': 'Github Users',
            },
        ),
        migrations.CreateModel(
            name='GitHubRepository',
            fields=[
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('id', models.PositiveBigIntegerField(unique=True)),
                ('owner', models.CharField(max_length=127)),
                ('name', models.CharField(max_length=127)),
                ('full_name', models.CharField(max_length=255)),
                ('description', models.TextField(null=True)),
                ('homepage', models.CharField(blank=True, max_length=255, null=True)),
                ('visibility', models.CharField(max_length=31)),
                ('watchers_count', models.IntegerField()),
                ('forks_count', models.IntegerField()),
                ('open_issues_count', models.IntegerField()),
                ('archived', models.BooleanField(default=False)),
                ('is_template', models.BooleanField(default=False)),
                ('language', models.CharField(max_length=127, null=True)),
                ('license_name', models.CharField(max_length=127, null=True)),
                ('disabled', models.BooleanField(default=False)),
                ('pushed_at', models.DateTimeField(null=True)),
                ('updated_at', models.DateTimeField(null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='repos', to='service.githubuser', to_field='id')),
            ],
            options={
                'verbose_name': 'Github Repository',
                'verbose_name_plural': 'Github Repositories',
            },
        ),
    ]
