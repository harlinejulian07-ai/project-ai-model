import datetime
import random
import os
import webbrowser

def greet_user(assistant_name, user_name):

    greetings = [
        f"{assistant_name}: Hello, {user_name}.",
        f"{assistant_name}: Welcome back, {user_name}.",
        f"{assistant_name}: Systems online.",
        f"{assistant_name}: Good to see you again.",
        f"{assistant_name}: Ready to assist."
    ]

    print(random.choice(greetings))


def tell_time(assistant_name):

    current_time = datetime.datetime.now().strftime("%I:%M %p")

    print(f"{assistant_name}: The current time is {current_time}.")


def system_status(assistant_name):

    print(f"{assistant_name}: Systems operating normally.")


def unknown_command(assistant_name):

    print(f"{assistant_name}: I do not recognize that command.")

def open_youtube(assistant_name):

    webbrowser.open("https://youtube.com")

    print(f"{assistant_name}: Opening YouTube.")

def open_google(assistant_name):

    webbrowser.open("https://google.com")

    print(f"{assistant_name}: Opening Google.")

def open_notepad(assistant_name):

    os.system("notepad")

    print(f"{assistant_name}: Opening Notepad.")
    