from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import PodcastEpisode
from .utils.audio import get_audio_duration

@receiver(post_save, sender=PodcastEpisode)
def process_episode(sender,instance,created,**kwargs):
    if created and instance.audio_file:
        file_path = instance.audio_file.path
        duration = get_audio_duration(file_path)
        instance.duration = duration
        instance.save()
    
