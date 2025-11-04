import pyttsx3
import speech_recognition as sr
from datetime import date
import time
import webbrowser
import datetime
from pynput.keyboard import Key, Controller
import pyautogui
import sys
import os
from os import listdir
from os.path import isfile, join
import smtplib
import wikipedia
import Gesture_Controller
#import Gesture_Controller_Gloved as Gesture_Controller
import app
from threading import Thread
import command_handler as cmd

# -------------Object Initialization---------------
today = date.today()
r = sr.Recognizer()
keyboard = Controller()
engine = pyttsx3.init('sapi5')
engine.setProperty('voice', engine.getProperty('voices')[0].id)

# ----------------Variables------------------------
file_exp_status = False
files = []
path = ''
is_awake = True  # Bot status

# ------------------Functions----------------------
def reply(audio):
    app.ChatBot.addAppMsg(audio)
    print(audio)
    engine.say(audio)
    engine.runAndWait()

def wish():
    hour = int(datetime.datetime.now().hour)
    if hour < 12:
        reply("Good Morning!")
    elif hour < 18:
        reply("Good Afternoon!")
    else:
        reply("Good Evening!")
    reply("I am Proton. How may I help you?")

def record_audio():
    with sr.Microphone() as source:
        print("\nListening...")
        r.adjust_for_ambient_noise(source, duration=1)
        r.pause_threshold = 0.8
        try:
            audio = r.listen(source, phrase_time_limit=8)
            print("Recognizing...")
            voice_data = r.recognize_google(audio)
            print("You said:", voice_data)
            return voice_data.lower()
        except sr.RequestError:
            reply('Sorry, my speech service is down. Please check your internet connection.')
        except sr.UnknownValueError:
            print("Didn't catch that — please speak again.")
        except Exception as e:
            print("Error during recognition:", e)
        return ""

# ------------------Command Handling-----------------
def handle_gesture_commands(voice_data):
    """Handles gesture-related voice commands"""
    if not Gesture_Controller.GestureController.gc_mode:
        reply("Gesture mode is inactive. Say 'launch gesture recognition' first.")
        return

    actions = {
        'move up': lambda: pyautogui.move(0, -100),
        'move down': lambda: pyautogui.move(0, 100),
        'move left': lambda: pyautogui.move(-100, 0),
        'move right': lambda: pyautogui.move(100, 0),
        'click': pyautogui.click,
        'double click': pyautogui.doubleClick,
        'scroll up': lambda: pyautogui.scroll(300),
        'scroll down': lambda: pyautogui.scroll(-300),
    }

    for key, action in actions.items():
        if key in voice_data:
            action()
            reply(f"Executed {key}")
            return True
    return False

def respond(voice_data):
    global file_exp_status, files, is_awake, path
    voice_data = voice_data.replace('rohan', '').replace('proton', '').strip()
    app.eel.addUserMsg(voice_data)

    if not is_awake:
        if 'wake up' in voice_data:
            is_awake = True
            wish()
        return

    # Gesture voice control
    if handle_gesture_commands(voice_data):
        return

    # ----------------Basic Static Commands----------------
    if 'hello' in voice_data:
        wish()

    elif 'what is your name' in voice_data:
        reply('My name is Proton!')

    elif 'date' in voice_data:
        reply(cmd.get_date())

    elif 'time' in voice_data or 'tell me the time' in voice_data:
        reply(cmd.get_time())

    elif 'search' in voice_data or 'google' in voice_data:
        query = voice_data.replace('search', '').replace('google', '').strip()
        if query:
            reply(f'Searching for {query}')
            cmd.google_search(query)
            reply('This is what I found')

    elif 'location' in voice_data:
        reply('Which place are you looking for?')
        temp_audio = record_audio()
        if temp_audio:
            app.eel.addUserMsg(temp_audio)
            url = f'https://www.google.com/maps/place/{temp_audio}'
            webbrowser.open(url)
            reply('This is what I found')

    elif ('bye' in voice_data) or ('goodbye' in voice_data):
        reply("Goodbye! Have a nice day.")
        is_awake = False

    elif 'exit' in voice_data or 'terminate' in voice_data:
        if Gesture_Controller.GestureController.gc_mode:
            Gesture_Controller.GestureController.gc_mode = 0
        app.ChatBot.close()
        sys.exit()

    # ----------------Gesture Activation----------------
    elif 'launch gesture' in voice_data or 'start gesture' in voice_data:
        if Gesture_Controller.GestureController.gc_mode:
            reply('Gesture recognition is already active.')
        else:
            gc = Gesture_Controller.GestureController()
            Thread(target=gc.start).start()
            reply('Gesture recognition launched successfully.')

    elif 'stop gesture' in voice_data:
        if Gesture_Controller.GestureController.gc_mode:
            Gesture_Controller.GestureController.gc_mode = 0
            reply('Gesture recognition stopped.')
        else:
            reply('Gesture recognition is already inactive.')

    # ----------------File Navigation----------------
    elif 'list' in voice_data:
        counter = 0
        path = 'C://'
        files.clear()
        files.extend(listdir(path))
        filestr = "".join(f"{i+1}: {f}<br>" for i, f in enumerate(files))
        file_exp_status = True
        reply('These are the files in your root directory.')
        app.ChatBot.addAppMsg(filestr)

    elif file_exp_status:
        counter = 0
        if 'open' in voice_data:
            try:
                index = int(voice_data.split()[-1]) - 1
                target = join(path, files[index])
                if isfile(target):
                    os.startfile(target)
                    file_exp_status = False
                else:
                    path = target + '//'
                    files[:] = listdir(path)
                    filestr = "".join(f"{i+1}: {f}<br>" for i, f in enumerate(files))
                    reply('Opened Successfully.')
                    app.ChatBot.addAppMsg(filestr)
            except Exception as e:
                reply('Unable to open file or directory.')

        elif 'back' in voice_data:
            if path == 'C://':
                reply('This is the root directory.')
            else:
                path = '//'.join(path.split('//')[:-2]) + '//'
                files[:] = listdir(path)
                filestr = "".join(f"{i+1}: {f}<br>" for i, f in enumerate(files))
                reply('Moved back.')
                app.ChatBot.addAppMsg(filestr)

    else:
        # 🔍 Fallback to Wikipedia for general questions
        try:
            reply('Let me check that for you...')
            summary = wikipedia.summary(voice_data, sentences=2)
            reply(summary)
        except Exception:
            reply('I am not functioned to do this yet!')

# ------------------Driver Code--------------------
t1 = Thread(target=app.ChatBot.start)
t1.start()

while not app.ChatBot.started:
    time.sleep(0.5)

wish()
voice_data = None

while True:
    voice_data = None
    is_gui_input = False

    if app.ChatBot.isUserInput():
        voice_data = app.ChatBot.popUserInput()
        is_gui_input = True
    else:
        voice_data = record_audio()

    if voice_data:
        wake_words = ['rohan', 'proton', 'wake up']
        has_wake_word = any(w in voice_data for w in wake_words)
        if has_wake_word or is_gui_input:
            try:
                respond(voice_data)
            except SystemExit:
                reply("Exit Successful")
                break
            except Exception as e:
                print("Exception during processing:", e)
