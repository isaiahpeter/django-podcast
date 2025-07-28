from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PodcastEpisodeViewSet, PodcastSeriesViewSet

router = DefaultRouter()
router.register(r'podcasts', PodcastEpisodeViewSet, basename='podcast')
router.register(r'podcasts', PodcastSeriesViewSet, basename='podcast_series')


urlpatterns = [
    path('', include(router.urls)),
]
