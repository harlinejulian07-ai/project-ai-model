# ==================================================
# JARVIS COMMAND MANAGER
# ==================================================

# ==================================================
# IMPORTS
# ==================================================

import datetime
import logging
import subprocess
import time

from plyer import notification
import speech_recognition as sr

from modules.youtube import run as youtube
from modules.google import run as google
from modules.system import get_time

from modules.notes import (
    open_notes,
    save_note as note_save,
    get_notes,
    clear_notes as note_clear
)

# ==================================================
# REMINDER SYSTEM
# ==================================================

def hourly_reminder_loop(assistant_name):

    while True:

        time.sleep(3600)

        send_notification(
            assistant_name,
            "Hourly reminder."
        )

        speak("Hourly reminder.")

# ==================================================
# VOICE SYSTEM
# ==================================================

listener = sr.Recognizer()

# ==================================================
# SPEECH SYSTEM
# ==================================================

def speak(text):

    try:

        safe_text = text.replace("'", "")

        subprocess.Popen(
            [
                "powershell",
                "-Command",
                f"""
                Add-Type -AssemblyName System.Speech;
                $voice = New-Object System.Speech.Synthesis.SpeechSynthesizer;
                $voice.Speak('{safe_text}')
                """
            ],
            creationflags=subprocess.CREATE_NO_WINDOW
        )

    except Exception as error:

        logging.error(f"TTS ERROR: {error}")

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
# VOICE RECOGNITION
# ==================================================

def listen_for_command():

    try:

        with sr.Microphone() as source:

            logging.info("Listening...")

            listener.adjust_for_ambient_noise(
                source,
                duration=1
            )

            audio = listener.listen(source)

        logging.info("Processing speech...")

        command = listener.recognize_google(audio)

        command = command.lower()

        logging.info(f"VOICE COMMAND: {command}")

        return command

    except Exception as error:

        logging.error(
            f"VOICE ERROR: {error}"
        )

        return None

# ==================================================
# BUILT-IN COMMANDS
# ==================================================

def tell_time(assistant_name):

    current_time = get_time()

    message = (
        f"The current time is {current_time}."
    )

    send_notification(
        assistant_name,
        message
    )

    speak(message)

def greet_user(
    assistant_name,
    user_name
):

    message = (
        f"Hello, {user_name}."
    )

    send_notification(
        assistant_name,
        message
    )

    speak(message)

def system_status(
    assistant_name
):

    message = (
        "Systems operating normally."
    )

    send_notification(
        assistant_name,
        message
    )

    speak(message)

def unknown_command(
    assistant_name
):

    message = (
        "I do not recognize that command."
    )

    send_notification(
        assistant_name,
        message
    )

    speak(message)

def open_notepad(assistant_name):

    notepad()

    send_notification(
        assistant_name,
        "Opening Notepad."
    )

    speak("Opening Notepad.")

# ==================================================
# MODULE WRAPPERS
# ==================================================

def open_youtube(
    assistant_name
):

    youtube()

    send_notification(
        assistant_name,
        "Opening YouTube."
    )

    speak("Opening YouTube.")

def open_google(
    assistant_name
):

    google()

    send_notification(
        assistant_name,
        "Opening Google."
    )

    speak("Opening Google.")

# ==================================================
# COMMAND REGISTRY
# ==================================================

COMMANDS = {

    # Greetings

    "hello": greet_user,
    "hi": greet_user,
    "hey": greet_user,

    # Time

    "time": tell_time,
    "clock": tell_time,

    # Status

    "status": system_status,
    "how are you": system_status,

    # YouTube

    "youtube": open_youtube,
    "yt": open_youtube,
    "open youtube": open_youtube,

    # Google

    "google": open_google,
    "search": open_google,
    "open google": open_google

}

# ==================================================
# NOTES
# ==================================================

def save_note(assistant_name):

    note = input("Enter note: ")

    note_save(note)

    send_notification(
        assistant_name,
        "Note saved."
    )

    speak("Note saved.")


def show_notes(assistant_name):

    notes = get_notes()

    if not notes:

        send_notification(
            assistant_name,
            "No notes found."
        )

        speak("No notes found.")

        return

    note_text = "\n".join(
        note.strip()
        for note in notes
    )

    send_notification(
        assistant_name,
        note_text
    )

    speak("Displaying notes.")


def clear_notes(assistant_name):

    note_clear()

    send_notification(
        assistant_name,
        "All notes cleared."
    )

    speak("All notes cleared.")