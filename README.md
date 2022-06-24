## About
This project is a quick scrapper using Github API that saves data in a chosen database and
exposes it through a REST API both built using Django Framework together with Django Rest Framework

## Quick Start (with docker)
1. Download the code :)
2. Setup github api key on env files present at root directory
3. Build image
`docker build . -t gh-user-data -f docker/Dockerfile`
4. Run migrations
```
docker run --rm --env-file docker/env \
           --mount source=gh_user_volume,target=/app \
           -p 8000:8000 gh-user-data \
           python manage.py migrate
```
5.  Fetch some data (first 10 users and their repos)
```
docker run --rm --env-file docker/env \
           --mount source=gh_user_volume,target=/app \
           gh-user-data python manage.py fetch_github_data
```
6. Create a user so you can explore data in admin
```
docker run --rm -it --env-file docker/env \
           --mount source=gh_user_volume,target=/app gh-user-data \
           python manage.py createsuperuser
```
7. Run the server
```
docker run --rm --env-file docker/env \
           --mount source=gh_user_volume,target=/app \
           -p 8000:8000 gh-user-data \
           python manage.py runserver 0.0.0.0:8000
```
8. Go to `http://localhost:8000/admin` or `http://localhost:8000/api/github/user`
9. Be happy :)

## Structure
The service is implemented using a Django project with one app that includes a
**Web Application** that can be queried for information about about users and
repositories through a REST API and a **Django Command** that can be executed to
scrape data from **Github api**.
#### Stack
1. Django
2. rest_framework
3. django_filters

#### REST API description
```
GET /api/github/user/ - List all users
GET /api/github/user/<uid>/ - Get a speficic user based on its uid (internal)
GET /api/github/user/?search=<query> - Search users (fields from available filters)
GET /api/github/user/?<field>=<value> - Filter results by
	login, location, name, email, company, bio, twitter_username,
	repos__name, repos__full_name, repos__language,

GET /api/github/repository/ - List all repositories
GET /api/github/repository/<uid>/ - Get a specific repository by uid (internal)
GET /api/github/repository/?search=<query> - Search repositoryes (fields from filters)
GET /api/github/repository/?<field>=<value> - Filter results by
	name, full_name, language, description, license_name, owner
```
#### Last coverage report
```
Name                                                          Stmts   Miss  Cover
---------------------------------------------------------------------------------
manage.py                                                         5      0   100%
service/__init__.py                                              19      2    89%
service/api/__init__.py                                          11      0   100%
service/api/commons.py                                           42      0   100%
service/api/repository.py                                        22      0   100%
service/api/user.py                                              30      1    97%
service/libs/__init__.py                                          0      0   100%
service/libs/github.py                                           38      1    97%
service/management/__init__.py                                    0      0   100%
service/management/commands/__init__.py                           0      0   100%
service/management/commands/fetch_github_data.py                 25      0   100%
service/migrations/0001_initial.py                                7      0   100%
service/migrations/0002_auto_20211025_2113.py                     5      0   100%
service/migrations/0003_alter_githubrepository_user.py            5      0   100%
service/migrations/0004_alter_githubuser_blog.py                  4      0   100%
service/migrations/0005_alter_githubrepository_homepage.py        4      0   100%
service/migrations/0006_auto_20211026_2212.py                     4      0   100%
service/migrations/0007_remove_githubrepository_watchers.py       4      0   100%
service/migrations/0008_auto_20211029_0004.py                     4      0   100%
service/migrations/__init__.py                                    0      0   100%
service/models.py                                                66      8    88%
service/tests/__init__.py                                         0      0   100%
service/tests/api/__init__.py                                     0      0   100%
service/tests/api/test_repository.py                             19      0   100%
service/tests/api/test_user.py                                   73      0   100%
service/tests/libs/__init__.py                                    0      0   100%
service/tests/libs/test_github.py                                20      0   100%
service/tests/management/__init__.py                              0      0   100%
service/tests/management/commands/__init__.py                     0      0   100%
service/tests/management/commands/test_fetch_github_data.py      36      0   100%
---------------------------------------------------------------------------------
TOTAL                                                           443     12    97%

```

#### Next Steps
* API: provide out of the box authentication/authorization for API
* API: allow enabling/disabling of admin site for leaner production deployments
* Scrapper: work with the since parameter of Github API to allow more specific scrapping strategies
* Scrapper: make it possible to run it in parallel
