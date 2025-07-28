from rest_framework import serializers
from .models import PodcastEpisode, PodcastSeries
from dj_rest_auth.registration.serializers import RegisterSerializer

class CustomRegisterSerializer(RegisterSerializer):
    _has_phone_field =False
        
class PodcastSeriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = PodcastSeries
        fields = ['id','title','slug','description']

class PodcastEpisodeSerializer(serializers.ModelSerializer):
    uploaded_by = serializers.ReadOnlyField(source='uploaded_by.username')
    series = PodcastSeriesSerializer(read_only=True)
    series_id = serializers.PrimaryKeyRelatedField(queryset=PodcastSeries.objects.all(),source='series', write_only=True, required=False)
    class Meta:
        model = PodcastEpisode
        fields = ['id', 'slug', 'title', 'description', 'audio_file', 'transcript', 'uploaded_by', 'uploaded_at','series', 'series_id','duration']
        read_only_fields = ['id', 'slug', 'uploaded_by', 'uploaded_at']
