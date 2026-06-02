import datetime
import random
import os
import webbrowser
import time

from plyer import notification

import speech_recognition as sr
import pyttsx3

# ==================================================
# VOICE SYSTEM
# ==================================================

def initialize_listener():

    return sr.Recognizer()


def initialize_voice_engine():

    return pyttsx3.init()


def speak(engine, text):

    engine.say(text)

    engine.runAndWait()


def listen_for_command(listener):

    try:

        with sr.Microphone() as source:

            print("Listening...")

            listener.adjust_for_ambient_noise(
                source,
                duration=1
            )

            audio = listener.listen(source)

        print("Processing speech...")

        command = listener.recognize_google(audio)

        command = command.lower()

        print(f"You said: {command}")

        return command

    except Exception as e:

        print(f"VOICE ERROR: {e}")

        return None

# ==================================================
# GREETING SYSTEM
# ==================================================

def greet_user(assistant_name, user_name):

    greetings = [

        f"Hello, {user_name}.",

        f"Welcome back, {user_name}.",

        "Systems online.",

        "Good to see you again.",

        "Ready to assist."
    ]

    message = random.choice(greetings)

    send_notification(
        assistant_name,
        message
    )

# ==================================================
# TIME SYSTEM
# ==================================================

def tell_time(assistant_name):

    current_time = datetime.datetime.now().strftime(
        "%I:%M %p"
    )

    send_notification(
        assistant_name,
        f"The current time is {current_time}."
    )

# ==================================================
# STATUS SYSTEM
# ==================================================

def system_status(assistant_name):

    send_notification(
        assistant_name,
        "Systems operating normally."
    )

# ==================================================
# ERROR HANDLING
# ==================================================

def unknown_command(assistant_name):

    send_notification(
        assistant_name,
        "I do not recognize that command."
    )

# ==================================================
# WEB COMMANDS
# ==================================================

def open_youtube(assistant_name):

    webbrowser.open("https://youtube.com")

    send_notification(
        assistant_name,
        "Opening YouTube."
    )


def open_google(assistant_name):

    webbrowser.open("https://google.com")

    send_notification(
        assistant_name,
        "Opening Google."
    )

# ==================================================
# APPLICATION COMMANDS
# ==================================================

def open_notepad(assistant_name):

    os.system("notepad")

    send_notification(
        assistant_name,
        "Opening Notepad."
    )

# ==================================================
# NOTE SYSTEM
# ==================================================

def save_note(assistant_name):

    note = input("Enter note: ")

    with open("notes/notes.txt", "a") as file:

        file.write(note + "\n")

    send_notification(
        assistant_name,
        "Note saved."
    )


def show_notes(assistant_name):

    try:

        with open("notes/notes.txt", "r") as file:

            notes = file.readlines()

        all_notes = "\n".join(
            note.strip() for note in notes
        )

        if all_notes == "":

            all_notes = "No notes found."

        send_notification(
            assistant_name,
            all_notes
        )

    except FileNotFoundError:

        send_notification(
            assistant_name,
            "No notes found."
        )


def clear_notes(assistant_name):

    with open("notes/notes.txt", "w") as file:

        file.write("")

    send_notification(
        assistant_name,
        "All notes cleared."
    )

# ==================================================
# NOTIFICATION SYSTEM
# ==================================================

def send_notification(title, message):

    notification.notify(
        title=title,
        message=message,
        timeout=10
    )

# ==================================================
# BACKGROUND REMINDER SYSTEM
# ==================================================

def hourly_reminder_loop(assistant_name):

    while True:

        time.sleep(3600)

        send_notification(
            assistant_name,
            "Hourly reminder."
        )