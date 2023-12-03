import pyttsx3
import pyttsx3
import speech_recognition as sr
import datetime
from twilio.rest import Client
from ecapture import ecapture as ec
from bs4 import BeautifulSoup
from urllib.request import urlopen



def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour>= 0 and hour<12:
        speak("Good Morning Sir !")
  
    elif hour>= 12 and hour<18:
        speak("Good Afternoon Ma'am !")   
  
    else:
        speak("Good Evening Sir !")  
  
    assname =("Sneha 1 point o")
    speak("I am your Assistant")
    speak(assname)

def username():
    speak("What should i call you ma'am")
    uname = takeCommand()
    speak("Welcome Mister")
    speak(uname)          
    speak("How can i Help you, Sir")

def takeCommand():
     
    r = sr.Recognizer()
     
    with sr.Microphone() as source:
         
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
  
    try:
        print("Recognizing...")    
        query = r.recognize_google(audio, language ='en-in')
        print(f"User said: {query}\n")
  
    except Exception as e:
        print(e)    
        print("Unable to Recognize your voice.")  
        return "None"
     
    return query


if __name__ == '__main__':
    wishMe()
    username()
     
    while True:
         
        query = takeCommand().lower()