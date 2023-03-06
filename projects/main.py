from stt import STT
from tasks import tasks
stt = STT()
task = tasks()
task.greet_me()
while True:
    audio = stt.record_audio()
    query = stt.transcribe(audio)
    task.process(query)
