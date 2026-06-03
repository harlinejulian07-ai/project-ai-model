import datetime
import random
import os
import webbrowser
import time

from plyer import notification

import speech_recognition as sr

# ==================================================
# VOICE SYSTEM
# ==================================================

listener = sr.Recognizer()


def speak(text):

    safe_text = text.replace("'", "")

    command = f'''
    PowerShell -Command "Add-Type -AssemblyName System.Speech;
    $voice = New-Object System.Speech.Synthesis.SpeechSynthesizer;
    $voice.Speak('{safe_text}')"
    '''

    os.system(command)


def listen_for_command():

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

    speak(message)

# ==================================================
# TIME SYSTEM
# ==================================================

def tell_time(assistant_name):

    current_time = datetime.datetime.now().strftime(
        "%I:%M %p"
    )

    message = f"The current time is {current_time}."

    send_notification(
        assistant_name,
        message
    )

    speak(message)

# ==================================================
# STATUS SYSTEM
# ==================================================

def system_status(assistant_name):

    message = "Systems operating normally."

    send_notification(
        assistant_name,
        message
    )

    speak(message)

# ==================================================
# ERROR HANDLING
# ==================================================

def unknown_command(assistant_name):

    message = "I do not recognize that command."

    send_notification(
        assistant_name,
        message
    )

    speak(message)

# ==================================================
# WEB COMMANDS
# ==================================================

def open_youtube(assistant_name):

    webbrowser.open("https://youtube.com")

    message = "Opening YouTube."

    send_notification(
        assistant_name,
        message
    )

    speak(message)


def open_google(assistant_name):

    webbrowser.open("https://google.com")

    message = "Opening Google."

    send_notification(
        assistant_name,
        message
    )

    speak(message)

# ==================================================
# APPLICATION COMMANDS
# ==================================================

def open_notepad(assistant_name):

    os.system("notepad")

    message = "Opening Notepad."

    send_notification(
        assistant_name,
        message
    )

    speak(message)

# ==================================================
# NOTE SYSTEM
# ==================================================

def save_note(assistant_name):

    note_window = input("Enter note: ")

    with open("notes/notes.txt", "a") as file:

        file.write(note_window + "\n")

    message = "Note saved."

    send_notification(
        assistant_name,
        message
    )

    speak(message)


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

        speak("Displaying notes.")

    except FileNotFoundError:

        send_notification(
            assistant_name,
            "No notes found."
        )

        speak("No notes found.")


def clear_notes(assistant_name):

    with open("notes/notes.txt", "w") as file:

        file.write("")

    message = "All notes cleared."

    send_notification(
        assistant_name,
        message
    )

    speak(message)

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

        speak("Hourly reminder.")