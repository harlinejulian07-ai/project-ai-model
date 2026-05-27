import datetime
import os
import webbrowser
import random

assistant_name = "JARVIS"

# ---------------- MEMORY SYSTEM ---------------- #

try:
    with open("brain/user_name.txt", "r") as file:
        user_name = file.read()

except:
    user_name = input(f"{assistant_name}: I don't know your name yet. What is your name? ")

    with open("brain/user_name.txt", "w") as file:
        file.write(user_name)

# ---------------- FUNCTIONS ---------------- #

def greet_user():

    greetings = [
        f"{assistant_name}: Hello, {user_name}.",
        f"{assistant_name}: Welcome back, {user_name}.",
        f"{assistant_name}: Systems online.",
        f"{assistant_name}: Good to see you again.",
        f"{assistant_name}: Ready to assist."
    ]

    print(random.choice(greetings))


def tell_time():

    current_time = datetime.datetime.now().strftime("%I:%M %p")

    print(f"{assistant_name}: The current time is {current_time}.")


def system_status():

    print(f"{assistant_name}: Systems operating normally.")


def unknown_command():

    print(f"{assistant_name}: I do not recognize that command.")


def open_youtube():

    webbrowser.open("https://youtube.com")

    print(f"{assistant_name}: Opening YouTube.")


def open_google():

    webbrowser.open("https://google.com")

    print(f"{assistant_name}: Opening Google.")


def open_notepad():

    os.system("notepad")

    print(f"{assistant_name}: Opening Notepad.")


def save_note():

    note = input("Enter note: ")

    with open("notes/notes.txt", "a") as file:
        file.write(note + "\n")

    print(f"{assistant_name}: Note saved.")


def show_notes():

    try:
        with open("notes/notes.txt", "r") as file:

            notes = file.readlines()

            print("\n--- NOTES ---")

            for note in notes:
                print(note.strip())

            print("-------------\n")

    except:
        print(f"{assistant_name}: No notes found.")


def clear_notes():

    with open("notes/notes.txt", "w") as file:
        file.write("")

    print(f"{assistant_name}: All notes cleared.")


# ---------------- STARTUP ---------------- #

print(f"{assistant_name}: Welcome back, {user_name}.")

# ---------------- COMMAND ROUTER ---------------- #

commands = {
    "hello": greet_user,
    "time": tell_time,
    "how are you": system_status,
    "youtube": open_youtube,
    "google": open_google,
    "notepad": open_notepad,
    "note": save_note,
    "show notes": show_notes,
    "clear notes": clear_notes
}

# ---------------- MAIN LOOP ---------------- #

while True:

    command = input(f"{assistant_name}: How can I assist you today? ").lower().strip()

    if command == "exit":

        print(f"{assistant_name}: Shutting down.")
        break

    elif command in commands:

        commands[command]()

    else:

        unknown_command()