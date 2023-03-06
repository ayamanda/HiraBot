import pyttsx3        

class tts:
    def __init__(self):
        self.engine = pyttsx3.init('sapi5')
        self.running = True

        # Setting the Voice
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[0].id)

        # Setting the Volume
        volume = self.engine.getProperty('volume')
        self.engine.setProperty('volume', 10.0)

        # Setting the Speed
        rate = self.engine.getProperty('rate')
        self.engine.setProperty('rate', rate - 50)

    # Function to speak text
    def speak(self, text):
        self.engine.say(text)
        self.engine.runAndWait()
