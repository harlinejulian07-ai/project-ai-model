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

ASSISTANT_NAME = "JARVIS"

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
    ASSISTANT_NAME,
    f"Welcome back, {user_name}."
)

speak("Systems online.")

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

    print(f"COMMAND RECEIVED: {command}")

    if command == "exit":

        os._exit(0)

    elif command in commands:

        execute_command(command)

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
                ASSISTANT_NAME,
                f"Did you mean '{matched_command}'?"
            )

            execute_command(matched_command)

        else:

            unknown_command(ASSISTANT_NAME)


def execute_command(command):

    command_function = commands[command]

    if command_function == greet_user:

        greet_user(
            ASSISTANT_NAME,
            user_name
        )

    else:

        command_function(ASSISTANT_NAME)

# ==================================================
# COMMAND WINDOW
# ==================================================

def open_command_window():

    global command_window_open

    if command_window_open:
        return

    command_window_open = True

    window = tk.Toplevel(root)

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

# ==================================================
# VOICE COMMANDS
# ==================================================

def voice_command():

    print("VOICE SYSTEM ACTIVATED")

    command = listen_for_command()

    if command:

        print(f"EXECUTING: {command}")

        process_command(command)

    else:

        print("NO COMMAND DETECTED")

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

    root.after(
        0,
        open_command_window
    )


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
    args=(ASSISTANT_NAME,),
    daemon=True
)

reminder_thread.start()

tray_thread = threading.Thread(
    target=setup_tray,
    daemon=True
)

tray_thread.start()

# ==================================================
# TKINTER ROOT
# ==================================================

root = tk.Tk()

root.withdraw()

# ==================================================
# HOTKEYS
# ==================================================

keyboard.add_hotkey(
    "ctrl+alt+j",
    lambda: root.after(0, open_command_window)
)

keyboard.add_hotkey(
    "ctrl+alt+v",
    lambda: threading.Thread(
        target=voice_command,
        daemon=True
    ).start()
)

# ==================================================
# MAIN LOOP
# ==================================================

root.mainloop()