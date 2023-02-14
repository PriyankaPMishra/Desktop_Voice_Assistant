import pyttsx3
import datetime
import speech_recognition as sr
import os
import random
import webbrowser
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import requests
import ctypes
import sys

engine = pyttsx3.init('sapi5')
rate = engine.getProperty('rate')
engine.setProperty('rate', 180)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)


# to get voice o/p
def speak(audio):
    engine.say(audio)
    engine.runAndWait()  # without this speech isnt audible


# Greeting The User
def wishMe():
    hour = int(datetime.datetime.now().hour)
    if (hour >= 0 and hour < 12):
        speak("Good Morning!")

    elif (hour >= 12 and hour < 16):
        speak("Good Afternoon!")

    else:
        speak("Good Evening !")
        print("Good Evening!")

    assname = "A"
    print("I am your assistant...", assname)
    speak("I am your Assistant.........")
    speak(assname)
    print("How shall I help you?")
    speak("How shall I help you?")


# Taking Voice COmmands from user
def takeCommand():
    r = sr.Recognizer()

    with sr.Microphone() as source:

        r.energy_threshold = 10000
        r.adjust_for_ambient_noise(source, 1.2)
        r.pause_threshold = 2
        print("Listening...")
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")

    except Exception as e:
        print(e)
        print("Unable to Recognize your voice.")
        return "None"

    return query


# Fetching information from Wikipedia
def get_info(topic):
    s = Service("C:\\Users\\Priyanka Mishra\\Downloads\\chromedriver_win32\\chromedriver.exe")
    browser = webdriver.Chrome(service=s)
    browser.get(url="https://www.wikipedia.org")
    search = browser.find_element(By.XPATH, '//*[@id="searchInput"]')
    search.click()
    search.send_keys(topic)
    enter = browser.find_element(By.XPATH, '//*[@id="search-form"]/fieldset/button')
    enter.click()
    time.sleep(600)


# Playing videos on YouTube
def get_yt_video(topic):
    s = Service("C:\\Users\\Priyanka Mishra\\Downloads\\chromedriver_win32\\chromedriver.exe")
    browser = webdriver.Chrome(service=s)
    browser.get(url="https://www.youtube.com/results?search_query=" + topic)
    video = browser.find_element(By.XPATH, "//*[@id='dismissible']")
    video.click()
    time.sleep(1000)


# Fetching latest News from JSON module and API
def news():
    key = '3cec628cce154ac393ed624cbb9e6072'
    api_address = 'https://newsapi.org/v2/top-headlines?country=in&apiKey=' + key
    json_data = requests.get(api_address).json()
    ar = []

    for i in range(3):
        t = "Number" + str(i + 1) + ": " + json_data["articles"][i]["title"] + "."
        ar.append(t)

    return ar


# Generating a random fact
def facts():
    limit = 1
    api_url = 'https://api.api-ninjas.com/v1/facts?limit={}'.format(limit)
    response = requests.get(api_url, headers={'X-Api-Key': '5YPgdV5JHXuBUNgGhokI+Q==6IOtWepMaDbWr1kf'})
    if response.status_code == requests.codes.ok:
        print(response.text)
        speak(response.text)
    else:
        print("Error:", response.status_code, response.text)


# defining weather conditions
def weather():
    city = takeCommand().lower()
    api_url = 'https://api.api-ninjas.com/v1/weather?city={}'.format(city)
    response = requests.get(api_url, headers={'X-Api-Key': '5YPgdV5JHXuBUNgGhokI+Q==6IOtWepMaDbWr1kf'})
    if response.status_code == requests.codes.ok:
        print(response.text)
    else:
        print("Error:", response.status_code, response.text)


if __name__ == "__main__":
    wishMe()
    while 1:
        query = takeCommand().lower()  # Converting user query into lower case
        # Logic for executing tasks based on query

        if 'wikipedia' in query:
            speak("What information do you need?")
            t = takeCommand().lower()
            speak(f'Searching Wikipedia... for{t}')
            query = get_info(t)

        if "news" in query:
            a = news()
            print("Reading headlines for you...")
            for i in a:
                print(i)
                speak(i)

        if "youtube" in query:
            speak("Which video do you want me to play?")
            t = takeCommand().lower()
            speak(f'Searching Youtube... for{t}')
            query = get_yt_video(t)

        if "play music" in query:
            speak("Playing a song...")
            m_dir = "D:\\songs"
            songs = os.listdir(m_dir)
            for s in songs:
                print(s)
            i = random.randint(0, len(songs) - 1)
            # print(i)
            os.startfile(os.path.join(m_dir, songs[i]))

        if "open google" in query:
            print("Opening google")
            speak("Opening google...")
            webbrowser.open("www.google.com")

        if "fact" in query:
            facts()

        if "weather" in query:
            speak("which city's weather do you need?")
            weather()

        if 'lock window' in query:
            speak("locking the device")
            ctypes.windll.user32.LockWorkStation()

        if 'exit' or 'stop' in query:
            speak("Thank You. Have a Good Day!")
            sys.exit()
