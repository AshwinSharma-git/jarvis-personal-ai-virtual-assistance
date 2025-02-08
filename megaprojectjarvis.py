
import speech_recognition as sr
import webbrowser
import pyttsx3
import requests
import musicLibrary 
import os
import pyautogui
import time
import datetime
import wikipedia
import pyjokes
import wolframalpha
import json
import psutil
import screen_brightness_control as sbc
from googletrans import Translator

# Initialize all APIs and clients
recognizer = sr.Recognizer()
engine = pyttsx3.init()
newsapi = "YOUR_NEWS_API_KEY"  # Replace with your key
WOLFRAM_APP_ID = "YOUR_WOLFRAM_ALPHA_API_KEY"  # Replace with your key
WEATHER_API_KEY = "YOUR_OPENWEATHERMAP_API_KEY"  # Replace with your key
wolfram_client = wolframalpha.Client(WOLFRAM_APP_ID)
translator = Translator()

def speak(text):
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.setProperty('rate', 150)
    engine.setProperty('volume', 1.0)
    engine.say(text)
    engine.runAndWait()

def listen():
    try:
        with sr.Microphone() as source:
            print("Listening...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source, timeout=5)
            return recognizer.recognize_google(audio)
    except sr.WaitTimeoutError:
        print("Listening timed out")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def choose_contact():
    speak("There are multiple contacts. Do you want to select the first or the second?")
    choice = listen()
    if "first" in choice.lower():
        pyautogui.press("down", presses=1)
    elif "second" in choice.lower():
        pyautogui.press("down", presses=2)
    else:
        speak("I didn't understand your choice. Selecting the first contact by default.")
    pyautogui.press("enter")
    time.sleep(1)

def open_whatsapp_app():
    try:
        speak("Opening WhatsApp application.")
        os.system("start whatsapp://")
        time.sleep(3)

        speak("Who do you want to message?")
        contact_name = listen()
        if not contact_name:
            speak("Sorry, I couldn't hear the contact name.")
            return

        pyautogui.hotkey('ctrl', 'f')
        time.sleep(0.5)
        pyautogui.typewrite(contact_name)
        time.sleep(1.5)

        if pyautogui.pixelMatchesColor(300, 400, (255, 255, 255)):
            pyautogui.press("enter")
        else:
            choose_contact()

        speak(f"What do you want to send to {contact_name}?")
        message = listen()
        if not message:
            speak("Sorry, I couldn't understand the message.")
            return

        pyautogui.typewrite(message)
        time.sleep(0.5)
        pyautogui.press("enter")
        speak("Message sent successfully!")

    except Exception as e:
        speak(f"An error occurred: {e}")
        print(f"Error: {e}")

def get_time():
    return datetime.datetime.now().strftime("%I:%M %p")

def get_date():
    return datetime.datetime.now().strftime("%B %d, %Y")

def get_system_stats():
    cpu_usage = psutil.cpu_percent()
    memory = psutil.virtual_memory()
    battery = psutil.sensors_battery()
    return f"CPU Usage: {cpu_usage}%, Memory Usage: {memory.percent}%, Battery: {battery.percent}%"

def get_weather(city):
    try:
        base_url = "http://api.openweathermap.org/data/2.5/weather"
        params = {
            'q': city,
            'appid': WEATHER_API_KEY,
            'units': 'metric'
        }
        response = requests.get(base_url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            temp = data['main']['temp']
            description = data['weather'][0]['description']
            humidity = data['main']['humidity']
            return f"Current weather in {city}: {description}, Temperature: {temp}°C, Humidity: {humidity}%"
        else:
            return "Unable to fetch weather information"
    except Exception as e:
        print(f"Weather error: {e}")
        return "Unable to fetch weather information"

def tell_joke():
    return pyjokes.get_joke()

def translate_text(text, target_lang):
    try:
        translation = translator.translate(text, dest=target_lang)
        return translation.text
    except:
        return "Translation failed"

def search_wikipedia(query):
    try:
        return wikipedia.summary(query, sentences=2)
    except:
        return "Could not find information on Wikipedia"

def control_brightness(level):
    try:
        sbc.set_brightness(level)
        return f"Brightness set to {level}%"
    except:
        return "Failed to adjust brightness"

def solve_math(query):
    try:
        res = wolfram_client.query(query)
        return next(res.results).text
    except:
        return "Could not solve the mathematical query"

def get_news():
    try:
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=us&apiKey={newsapi}")
        if r.status_code == 200:
            data = r.json()
            articles = data.get('articles', [])
            return articles[:5]
        return None
    except:
        return None

def processCommand(command):
    if "open google" in command.lower():
        speak("Google is ready to help, let's search!")
        webbrowser.open("https://google.com")
        speak("What would you like to search for?")
        
        search_query = listen()
        if search_query:
            speak(f"Searching Google for {search_query}")
            search_url = f"https://www.google.com/search?q={search_query}"
            webbrowser.open(search_url)
        else:
            speak("Sorry, I couldn't understand your search query.")

    elif "open youtube" in command.lower():
        speak("Okay, rolling the YouTube red carpet for you!")
        webbrowser.open("https://youtube.com")
        speak("What would you like to search for on YouTube?")
        
        search_query = listen()
        if search_query:
            speak(f"Searching YouTube for {search_query}")
            search_url = f"https://www.youtube.com/results?search_query={search_query}"
            webbrowser.open(search_url)
        else:
            speak("Sorry, I couldn't understand your search query.")

    elif "open linkedin" in command.lower():
        speak("Okay, opening LinkedIn. Let's make those connections!")
        webbrowser.open("https://linkedin.com")

    elif "open whatsapp" in command.lower():
        open_whatsapp_app()

    elif "open instagram" in command.lower():
        speak("Okay, it's time for some Insta magic! Let's see some posts.")
        webbrowser.open("https://instagram.com")

    elif command.lower().startswith("play"):
        song = command.lower().split(" ")[1]
        link = musicLibrary.music[song]
        speak("Music mode activated, let's jam!")
        webbrowser.open(link)

    elif "news" in command.lower():
        speak("Here are the top headlines:")
        articles = get_news()
        if articles:
            for article in articles:
                speak(article['title'])
        else:
            speak("Sorry, I couldn't fetch the latest news.")

    elif "time" in command.lower():
        current_time = get_time()
        speak(f"The current time is {current_time}")

    elif "date" in command.lower():
        current_date = get_date()
        speak(f"Today is {current_date}")

    elif "system stats" in command.lower() or "system status" in command.lower():
        stats = get_system_stats()
        speak(stats)

    elif "weather" in command.lower():
        speak("Which city would you like to know the weather for?")
        city = listen()
        if city:
            weather_info = get_weather(city)
            speak(weather_info)

    elif "joke" in command.lower() or "make me laugh" in command.lower():
        joke = tell_joke()
        speak(joke)

    elif "translate" in command.lower():
        speak("What would you like me to translate?")
        text = listen()
        if text:
            speak("To which language? For example, say 'spanish' or 'french'")
            lang = listen()
            if lang:
                translation = translate_text(text, lang.lower())
                speak(f"The translation is: {translation}")

    elif "wikipedia" in command.lower() or "search for" in command.lower():
        speak("What would you like to search on Wikipedia?")
        query = listen()
        if query:
            result = search_wikipedia(query)
            speak(result)

    elif "brightness" in command.lower():
        speak("What brightness level would you like? Say a number between 0 and 100")
        level = listen()
        if level and level.isdigit():
            result = control_brightness(int(level))
            speak(result)

    elif "calculate" in command.lower() or "solve" in command.lower():
        speak("What would you like me to calculate?")
        query = listen()
        if query:
            result = solve_math(query)
            speak(f"The answer is {result}")

    else:
        speak("I'm not sure how to help with that. Could you please try another command?")

if __name__ == "__main__":
    speak("Initializing virtual assistant... Hello! I am Jarvis, an advanced AI assistant designed and developed by Ashwin Sharma. I'm here to enhance your digital experience.")
    speak("Here are some things I can do for you:")
    speak("1. Open and search on websites like Google, YouTube, LinkedIn, and Instagram")
    speak("2. Send WhatsApp messages")
    speak("3. Play music")
    speak("4. Get latest news")
    speak("5. Check time and date")
    speak("6. Monitor system statistics")
    speak("7. Get weather updates")
    speak("8. Tell jokes")
    speak("9. Translate text")
    speak("10. Search Wikipedia")
    speak("11. Control screen brightness")
    speak("12. Solve mathematical problems")
    speak("Just say 'Jarvis' followed by your command!")

    while True:
        print("Recognizing...")
        try:
            with sr.Microphone() as source:
                print("Listening for wake word...")
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source)
            word = recognizer.recognize_google(audio)
            if word.lower() == "jarvis":
                speak("Yes, sir! How may I help you?")
                
                with sr.Microphone() as source:
                    print("Jarvis active...")
                    audio = recognizer.listen(source)
                    command = recognizer.recognize_google(audio)
                    processCommand(command)
        except Exception as e:
            print(f"Error: {e}")