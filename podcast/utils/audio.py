from pydub import AudioSegment
import datetime
#import whisper

#model = whisper.load_model('base')

def get_audio_duration(file_path):
    audio = AudioSegment.from_file(file_path)
    seconds = len(audio)/1000
    return datetime.timedelta(seconds=seconds)
    
#def transcribe_audio(file_path):
  #  result = model.transcribe(file_path)
   # return result['text']


