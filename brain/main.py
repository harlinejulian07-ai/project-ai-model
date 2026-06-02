from commands import *

from pystray import Icon, MenuItem, Menu
from PIL import Image, ImageDraw

import tkinter as tk
import threading
import keyboard
import difflib
import time
import os

# ==================================================
# CONFIG
# ==================================================

assistant_name = "JARVIS"

# ==================================================
# VOICE SYSTEM
# ==================================================

listener = initialize_listener()

voice_engine = initialize_voice_engine()

# ==================================================
# WINDOW STATE
# ==================================================

command_window_open = False

# ==================================================
# MEMORY SYSTEM
# ==================================================

def load_user_name():

    try:

        with open("brain/user_name.txt", "r") as file:

            return file.read().strip()

    except FileNotFoundError:

        return None


def save_user_name(name):

    with open("brain/user_name.txt", "w") as file:

        file.write(name)


user_name = load_user_name()

# ==================================================
# FIRST TIME SETUP
# ==================================================

if not user_name:

    setup_window = tk.Tk()

    setup_window.title("JARVIS Setup")

    setup_window.geometry("350x150")

    setup_window.attributes("-topmost", True)

    label = tk.Label(
        setup_window,
        text="What is your name?"
    )

    label.pack(pady=10)

    name_entry = tk.Entry(
        setup_window,
        width=30
    )

    name_entry.pack(pady=10)

    name_entry.focus()

    def submit_name():

        global user_name

        user_name = name_entry.get().strip()

        save_user_name(user_name)

        setup_window.destroy()

    submit_button = tk.Button(
        setup_window,
        text="Save",
        command=submit_name
    )

    submit_button.pack(pady=10)

    setup_window.mainloop()

# ==================================================
# STARTUP SEQUENCE
# ==================================================

startup_messages = [

    "Initializing JARVIS...",

    "Loading core systems...",

    "Checking memory banks...",

    "Establishing command router...",

    "Systems online."
]

for message in startup_messages:

    print(message)

    time.sleep(1)

send_notification(
    assistant_name,
    f"Welcome back, {user_name}."
)

speak(
    voice_engine,
    "Systems online."
)

# ==================================================
# COMMAND ROUTER
# ==================================================

commands = {

    # Greetings
    "hello": greet_user,
    "hi": greet_user,
    "hey": greet_user,

    # Time
    "time": tell_time,
    "clock": tell_time,

    # YouTube
    "youtube": open_youtube,
    "yt": open_youtube,
    "open youtube": open_youtube,
    "launch youtube": open_youtube,

    # Google
    "google": open_google,
    "search": open_google,
    "open google": open_google,

    # Notepad
    "notepad": open_notepad,
    "open notepad": open_notepad,

    # Notes
    "note": save_note,
    "show notes": show_notes,
    "clear notes": clear_notes
}

# ==================================================
# COMMAND PROCESSOR
# ==================================================

def process_command(command):

    command = command.lower().strip()

    if command == "exit":

        os._exit(0)

    elif command in commands:

        if commands[command] == greet_user:

            greet_user(
                assistant_name,
                user_name
            )

        elif commands[command] == save_note:

            save_note(
                assistant_name
            )

        else:

            commands[command](assistant_name)

    else:

        possible_matches = difflib.get_close_matches(
            command,
            commands.keys(),
            n=1,
            cutoff=0.6
        )

        if possible_matches:

            matched_command = possible_matches[0]

            send_notification(
                assistant_name,
                f"Did you mean '{matched_command}'?"
            )

            if commands[matched_command] == greet_user:

                greet_user(
                    assistant_name,
                    user_name
                )

            elif commands[matched_command] == save_note:

                save_note(
                    assistant_name
                )

            else:

                commands[matched_command](assistant_name)

        else:

            unknown_command(assistant_name)

# ==================================================
# COMMAND WINDOW
# ==================================================

def open_command_window():

    global command_window_open

    if command_window_open:
        return

    command_window_open = True

    window = tk.Tk()

    window.title("JARVIS")

    window.geometry("400x140")

    window.attributes("-topmost", True)

    label = tk.Label(
        window,
        text="Enter Command"
    )

    label.pack(pady=10)

    entry = tk.Entry(
        window,
        width=40
    )

    entry.pack(pady=5)

    entry.focus()

    def close_window():

        global command_window_open

        command_window_open = False

        window.destroy()

    def submit_command(event=None):

        command = entry.get()

        process_command(command)

        close_window()

    window.protocol(
        "WM_DELETE_WINDOW",
        close_window
    )

    entry.bind("<Return>", submit_command)

    submit_button = tk.Button(
        window,
        text="Execute",
        command=submit_command
    )

    submit_button.pack(pady=10)

    window.mainloop()

# ==================================================
# VOICE COMMANDS
# ==================================================

def voice_command():

    command = listen_for_command(listener)

    if command:

        print(f"Executing: {command}")

        process_command(command)

    else:

        print("No command detected.")
# ==================================================
# SYSTEM TRAY
# ==================================================

def create_image():

    image = Image.new(
        "RGB",
        (64, 64),
        color="black"
    )

    draw = ImageDraw.Draw(image)

    draw.ellipse(
        (16, 16, 48, 48),
        fill="cyan"
    )

    return image


def quit_jarvis(icon, item):

    icon.stop()

    os._exit(0)


def open_command_from_tray(icon, item):

    threading.Thread(
        target=open_command_window,
        daemon=True
    ).start()


def setup_tray():

    tray_icon = Icon(
        "JARVIS",
        create_image(),
        "JARVIS Assistant",
        menu=Menu(

            MenuItem(
                "Open Command Window",
                open_command_from_tray
            ),

            MenuItem(
                "Quit",
                quit_jarvis
            )
        )
    )

    tray_icon.run()

# ==================================================
# BACKGROUND THREADS
# ==================================================

reminder_thread = threading.Thread(
    target=hourly_reminder_loop,
    args=(assistant_name,),
    daemon=True
)

reminder_thread.start()

tray_thread = threading.Thread(
    target=setup_tray,
    daemon=True
)

tray_thread.start()

# ==================================================
# HOTKEYS
# ==================================================

keyboard.add_hotkey(
    "ctrl+alt+j",
    open_command_window
)

keyboard.add_hotkey(
    "ctrl+alt+v",
    voice_command
)

# ==================================================
# KEEP APP RUNNING
# ==================================================

keyboard.wait()