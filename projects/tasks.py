import datetime
import json
import requests
from bs4 import BeautifulSoup
import random
import webbrowser
import wolframalpha
import pafy
import requests
import pyglet
import urllib.request
import spacy
import io
import os
import re, requests, subprocess, urllib.parse, urllib.request
from tts import tts
from stt import STT
stt=STT()
tts=tts()

class tasks:
    def __init__(self):
        self.name = "Ayan"
        self.nlp = spacy.load("en_core_web_sm")

    def greet_me(self):
        current_hour = int(datetime.datetime.now().hour)
        if 0 <= current_hour < 6:
            tts.speak("Good night! " + self.name)
        elif 6 <= current_hour < 12:
            tts.speak("Good morning! " + self.name)
        elif 12 <= current_hour < 18:
            tts.speak("Good afternoon! " + self.name)
        else:
            tts.speak("Good evening! " + self.name)

        greetings = ["How can I help you today?", "What can I do for you?", "How can I assist you?", "What do you need?", "Is there anything I can help you with?"]
        tts.speak(random.choice(greetings))

   

    # Function to search YouTube
    def youtubeSearch(self,query):
        tts.speak("Hold on, I will search YouTube for you.")
        query = query.replace("search", "")
        query = query.replace("YouTube", "")
        clip2 = self.urlext(query) # the function `urlext` is not defined in the code
        if len(clip2)>0:
            webbrowser.open(clip2)
        else:
            webbrowser.open(f"https://www.youtube.com/results?search_query={query}")


    # Function to open websites
    def openWebsite(self,query):
        query = query.lower()
        tts.speak("Hold on, I will open the website for you.")
        if "pw" in query:
            url = "https://www.pw.live/study/batches/arjuna-jee-2023-426578/batch-overview"
            try:
                webbrowser.open(url)
                return
            except Exception as e:
                tts.speak("Sorry, I was unable to open the website. Could you please check the link and try again?")
                print(e)

        query = query.replace("open website", "")
        # check if query contains specific TLDs
        if all(
            ext not in query
            for ext in [".com", ".org", ".edu", ".gov", ".in", ".live", ".io", ".ly", ".ai", ".app", ".dev", ".ac", ".ag", ".am", ".at", ".be", ".biz", ".bz", ".cc", ".cn", ".de", ".dk", ".es", ".eu", ".fm", ".fr", ".gs", ".info", ".it", ".jobs", ".jp", ".li", ".me", ".mobi", ".ms", ".name", ".net", ".nl", ".nu", ".pl", ".pro", ".pt", ".ru", ".se", ".sg", ".sh", ".tv", ".tw", ".us", ".co", ".uk"]
        ):
            query += ".com"
        if "https" not in query and "http" not in query:
            query = f"https://{query}"
        try:
            webbrowser.open(query)
        except Exception as e:
            tts.speak("Sorry, I was unable to open the website. Could you please check the spelling and try again?")
            print(e)


    # Function to speak the date and time
    def speakDateTime(self):
        now = datetime.datetime.now()
        tts.speak("Current date is "+ now.strftime("%B %d, %Y")+ " and the time is "+ now.strftime("%H:%M:%S"))

    # Function to talk like a friend

    def friendTalk(self):
        greetings = ["What's up? How are you doing today?", "How's your day going?", "How are you feeling today?", "What's on your mind?", "What have you been up to?"]
        self(random.choice(greetings))


    # Function to get the results from Dictionary


    def dictionary(self, query):
        # Extract the topic from the query
        query_parts = query.split(' in ')
        word = query_parts[0].replace('define ', '').strip()
        topic = query_parts[1].strip() if len(query_parts) > 1 else None

        # Format the word and topic as part of the URL
        url = f'https://www.google.com/search?q=define+{word}'
        if topic:
            url += f'+in+{topic}'

        # Send a GET request to the URL and get the HTML content of the page
        response = requests.get(url)

        # Check if the request was successful
        if response.status_code != 200:
            raise ValueError(f'Request failed with status code {response.status_code}')

        html_content = response.content

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')

        # Find the first div element containing the definition
        definition_div = soup.find('div', {'class': 'BNeawe s3v9rd AP7Wnd'})

        # Extract the text of the definition
        if definition_div is not None:
            definition = definition_div.get_text()
            tts.speak(f'Definition of "{word}": {definition}')
        else:
            tts.speak(f'No definitions found for "{word}"')


    # Function to get answers from WolframAlpha
    def getWolframAlpha(self,query):
        app_id = "KP3R8E-EEKW7P86HJ"
        client = wolframalpha.Client(app_id)
        res = client.query(query)
        answer = next(res.results).text
        tts.speak(answer)

    def exitCommand(self, my_command,query):
        query = query.lower()
        if "quit" in query or "exit" in query:
            tts.speak("Bye! Have a nice day.")
            tts.speak("Do you want me to turn off or keep running in the background?")
            query = my_command()
            query = query.lower()
            if "off" in query or "turn off" in query:
                tts.speak("Turning off, have a good day.")
                exit()
            elif "background" in query:
                tts.speak("I will keep running in the background.")
            else:
                tts.speak("Invalid command, I will keep running in the background.")

    def play_song(self,query):
        query = query.replace("play music", "")
        music_name = query
        clip2 = self.urlext(music_name)
        url = str(clip2)
        video = pafy.new(url)
        bestaudio = video.getbestaudio()
        playurl = bestaudio.url

        with urllib.request.urlopen(playurl) as response:
            song_data = io.BytesIO(response.read())

        player = pyglet.media.Player()
        song = pyglet.media.load(os.path.abspath(song_data.name), streaming=False)
        player.queue(song)
        player.play()

        while True:
            command = stt.transcribe()
            print(f"You said: {command}")
            if 'pause' in command:
                player.pause()
                print("Audio Paused")
            elif 'resume' in command:
                player.play()
                print("Audio Resumed")
            elif 'volume up' in command:
                current_volume = player.volume
                player.volume = min(current_volume + 0.1, 1.0)
                print("Volume increased")
            elif 'volume down' in command:
                current_volume = player.volume
                player.volume = max(current_volume - 0.1, 0.0)
                print("Volume decreased")
            elif 'next song' in command:
                player.next()
                print("Playing next song")
            elif 'exit' in command:
                player.pause()
                print("Exiting program")
                break
            else:
                print("Sorry, I did not understand what you said.")

    # TODO Rename this here and in `youtubeSearch` and `play_song`
    def urlext(self, arg0):
        query_string = urllib.parse.urlencode({"search_query": arg0})
        formatUrl = urllib.request.urlopen(
            f"https://www.youtube.com/results?{query_string}"
        )
        search_results = re.findall("watch\?v=(\S{11})", formatUrl.read().decode())
        clip = requests.get(f"https://www.youtube.com/watch?v={search_results[0]}")
        result = f"https://www.youtube.com/watch?v={search_results[0]}"
        print(result)
        return result
    

    def process(self, query):
        query = query.lower()
        doc = self.nlp(query)

        # Extract verb and noun chunks from the query
        verb_chunks = [chunk.text for chunk in doc.noun_chunks if chunk.root.pos_ == "VERB"]
        noun_chunks = [chunk.text for chunk in doc.noun_chunks if chunk.root.pos_ == "NOUN"]

        # Check if any verbs or nouns were found in the query
        if verb_chunks:
            verb = verb_chunks[0]
        else:
            verb = None

        if noun_chunks:
            noun = noun_chunks[0]
        else:
            noun = None

        # Perform actions based on the extracted verb and noun
        if verb == "open":
            if "website" in noun:
                self.openWebsite(query)
            elif "youtube" in noun:
                self.youtubeSearch(query)

        elif verb == "define":
            if noun:
                self.dictionary(noun)

        elif verb == "calculate":
            if noun:
                self.getWolframAlpha(noun)

        elif verb == "play":
            if noun == "music":
                self.play_song(query)

        elif "date" in query and "time" in query:
            self.speakDateTime()

        elif "talk like a friend" in query:
            self.friendTalk()

        elif "quit" in query:
            self.exitCommand()

        else:
            tts.speak("I'm sorry, I didn't understand your query.")




