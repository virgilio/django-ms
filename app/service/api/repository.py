from django.urls.conf import include, path
from django.contrib import admin

from rest_framework import routers, serializers, viewsets, filters, mixins
from django_filters import rest_framework as drf_filters

from service.api.commons import GitHubSerializerMixin
from service.models import GitHubRepository


class GitHubRepositorySerializer(GitHubSerializerMixin,
                                 serializers.ModelSerializer):

    class Meta:
        model = GitHubRepository
        fields = '__all__'


class GitHubRepositoryViewSet(mixins.RetrieveModelMixin,
                              mixins.ListModelMixin,
                              viewsets.GenericViewSet):
    serializer_class = GitHubRepositorySerializer
    queryset = GitHubRepository.objects.all()
    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
        drf_filters.DjangoFilterBackend
    ]
    filterset_fields = search_fields = [
        'name', 'full_name', 'language', 'description', 'license_name', 'owner'
    ]

    class Meta:
        pass


class GithubRepositoryAdmin(admin.ModelAdmin):
    pass


router = routers.DefaultRouter()
router.register(r'', GitHubRepositoryViewSet, basename='GithubRepository')
urlpatters = [
    path('', include(router.urls)),
], 'service', 'repositories'
