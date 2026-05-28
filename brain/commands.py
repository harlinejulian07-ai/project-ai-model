import datetime
import random
import os
import webbrowser
import time

from plyer import notification

# ---------------- GREETING SYSTEM ---------------- #

def greet_user(assistant_name, user_name):

    greetings = [

        f"{assistant_name}: Hello, {user_name}.",

        f"{assistant_name}: Welcome back, {user_name}.",

        f"{assistant_name}: Systems online.",

        f"{assistant_name}: Good to see you again.",

        f"{assistant_name}: Ready to assist."
    ]

    print(random.choice(greetings))

# ---------------- TIME SYSTEM ---------------- #

def tell_time(assistant_name):

    current_time = datetime.datetime.now().strftime("%I:%M %p")

    print(
        f"{assistant_name}: The current time is {current_time}."
    )

# ---------------- STATUS SYSTEM ---------------- #

def system_status(assistant_name):

    print(
        f"{assistant_name}: Systems operating normally."
    )

# ---------------- ERROR HANDLING ---------------- #

def unknown_command(assistant_name):

    print(
        f"{assistant_name}: I do not recognize that command."
    )

# ---------------- WEB COMMANDS ---------------- #

def open_youtube(assistant_name):

    webbrowser.open("https://youtube.com")

    print(
        f"{assistant_name}: Opening YouTube."
    )


def open_google(assistant_name):

    webbrowser.open("https://google.com")

    print(
        f"{assistant_name}: Opening Google."
    )

# ---------------- APPLICATION COMMANDS ---------------- #

def open_notepad(assistant_name):

    os.system("notepad")

    print(
        f"{assistant_name}: Opening Notepad."
    )

# ---------------- NOTE SYSTEM ---------------- #

def save_note(assistant_name):

    note = input("Enter note: ")

    with open("notes/notes.txt", "a") as file:

        file.write(note + "\n")

    print(
        f"{assistant_name}: Note saved."
    )


def show_notes(assistant_name):

    try:

        with open("notes/notes.txt", "r") as file:

            notes = file.readlines()

        print("\n--- NOTES ---")

        for note in notes:

            print(note.strip())

        print("-------------\n")

    except FileNotFoundError:

        print(
            f"{assistant_name}: No notes found."
        )


def clear_notes(assistant_name):

    with open("notes/notes.txt", "w") as file:

        file.write("")

    print(
        f"{assistant_name}: All notes cleared."
    )

# ---------------- NOTIFICATION SYSTEM ---------------- #

def send_notification(title, message):

    notification.notify(
        title=title,
        message=message,
        timeout=10
    )

# ---------------- BACKGROUND REMINDER SYSTEM ---------------- #

def hourly_reminder_loop(assistant_name):

    while True:

        time.sleep(3600)

        send_notification(
            "JARVIS",
            "Hourly reminder."
        )