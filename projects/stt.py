import speech_recognition as sr
import torch
from pydub import AudioSegment
import numpy as np
import whisper


class STT:
    def __init__(self):
        self.r = sr.Recognizer()
        self.r.energy_threshold = 300
        self.r.pause_threshold = 0.8
        self.r.dynamic_energy_threshold = False
        self.audio_model = whisper.load_model("base")

    def record_audio(self):
        with sr.Microphone(sample_rate=16000) as source:
            print("Say something!")
            i = 0
            #get and save audio to wav file
            audio = self.r.listen(source)
            torch_audio = torch.from_numpy(np.frombuffer(audio.get_raw_data(), np.int16).flatten().astype(np.float32) / 32768.0)
            audio_data = torch_audio
        return audio_data

    def transcribe(self, audio):
        audio_data = audio
        result = self.audio_model.transcribe(audio_data) #English model

        predicted_text = result["text"]
        print(predicted_text)
        return predicted_text
#, language='english'