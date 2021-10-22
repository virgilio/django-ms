from django.urls import path, include
from django.contrib import admin

from rest_framework import viewsets, serializers, routers, filters, mixins
from django_filters import rest_framework as drf_filters

from service.api.repository import GitHubRepositorySerializer
from service.api.commons import GitHubSerializerMixin
from service.models import GitHubUser


class GitHubUserSerializer(GitHubSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = GitHubUser
        fields = '__all__'


class GitHubUserFullSerializer(serializers.ModelSerializer):
    repos = GitHubRepositorySerializer(many=True)

    class Meta:
        model = GitHubUser
        fields = '__all__'


class GitHubUserViewSet(mixins.RetrieveModelMixin,
                        mixins.ListModelMixin,
                        viewsets.GenericViewSet):
    serializer_class = GitHubUserSerializer
    queryset = GitHubUser.objects.all()
    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
        drf_filters.DjangoFilterBackend
    ]
    filterset_fields = search_fields = [
        'login', 'location', 'name', 'email', 'company', 'bio',
        'twitter_username', 'repos__name', 'repos__full_name',
        'repos__language',
    ]

    def get_serializer_class(self):
        if self.action in ('retrieve', 'list'):
            return GitHubUserFullSerializer
        return super().get_serializer_class()


class GitHubUserAdmin(admin.ModelAdmin):
    pass


router = routers.DefaultRouter()
router.register(r'', GitHubUserViewSet, basename='GithubUser')
urlpatters = [
    path('', include(router.urls)),
], 'service', 'users'
