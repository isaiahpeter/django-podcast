from django.contrib import admin
from .models import PodcastEpisode, PodcastSeries
@admin.register(PodcastSeries)
class PodcastSeriesAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')
    prepopulated_fields ={'slug':('title',)}

@admin.register(PodcastEpisode)
class PodcastEpisodeAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'uploaded_by', 'duration')
    prepopulated_fields = {'slug':('title',)}

