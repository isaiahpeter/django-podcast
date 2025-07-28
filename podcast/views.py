from rest_framework import viewsets, permissions
from .models import PodcastEpisode,PodcastSeries
from .serializers import PodcastEpisodeSerializer, PodcastSeriesSerializer

class PodcastEpisodeViewSet(viewsets.ModelViewSet):
    queryset = PodcastEpisode.objects.all()
    serializer_class = PodcastEpisodeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'

    def perform_create(self, serializer):
        serializer.save(uploaded_by=self.request.user)

class PodcastSeriesViewSet(viewsets.ModelViewSet):
    queryset = PodcastSeries.objects.all()
    serializer_class = PodcastSeriesSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'
    def perform_create(self, serializer):
        serializer.save(uploaded_by=self.request.user)

