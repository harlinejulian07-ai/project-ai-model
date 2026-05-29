from commands import *

from pystray import Icon, MenuItem, Menu
from PIL import Image, ImageDraw

import tkinter as tk
import threading
import keyboard
import time
import os

# ==================================================
# CONFIG
# ==================================================

assistant_name = "JARVIS"

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

if not user_name:

    root = tk.Tk()

    root.withdraw()

    popup = tk.Toplevel()

    popup.title("JARVIS Setup")

    popup.geometry("350x120")

    popup.attributes("-topmost", True)

    label = tk.Label(
        popup,
        text="What is your name?"
    )

    label.pack(pady=10)

    name_entry = tk.Entry(
        popup,
        width=30
    )

    name_entry.pack(pady=5)

    name_entry.focus()

    def submit_name():

        global user_name

        user_name = name_entry.get().strip()

        save_user_name(user_name)

        popup.destroy()

    submit_button = tk.Button(
        popup,
        text="Save",
        command=submit_name
    )

    submit_button.pack(pady=10)

    popup.mainloop()

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
    "JARVIS",
    f"Welcome back, {user_name}."
)

# ==================================================
# COMMAND ROUTER
# ==================================================

commands = {

    "hello": lambda: greet_user(
        assistant_name,
        user_name
    ),

    "time": lambda: tell_time(
        assistant_name
    ),

    "how are you": lambda: system_status(
        assistant_name
    ),

    "youtube": lambda: open_youtube(
        assistant_name
    ),

    "google": lambda: open_google(
        assistant_name
    ),

    "notepad": lambda: open_notepad(
        assistant_name
    ),

    "note": lambda: save_note(
        assistant_name
    ),

    "show notes": lambda: show_notes(
        assistant_name
    ),

    "clear notes": lambda: clear_notes(
        assistant_name
    )
}

# ==================================================
# COMMAND PROCESSOR
# ==================================================

def process_command(command):

    command = command.lower().strip()

    if command == "exit":

        os._exit(0)

    elif command in commands:

        commands[command]()

    else:

        unknown_command(assistant_name)

# ==================================================
# COMMAND WINDOW
# ==================================================

def open_command_window():

    window = tk.Tk()

    window.title("JARVIS")

    window.geometry("400x120")

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

    def submit_command(event=None):

        command = entry.get()

        process_command(command)

        window.destroy()

    entry.bind("<Return>", submit_command)

    submit_button = tk.Button(
        window,
        text="Execute",
        command=submit_command
    )

    submit_button.pack(pady=10)

    window.mainloop()

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
# BACKGROUND REMINDERS
# ==================================================

reminder_thread = threading.Thread(
    target=hourly_reminder_loop,
    args=(assistant_name,),
    daemon=True
)

reminder_thread.start()

# ==================================================
# TRAY THREAD
# ==================================================

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

# ==================================================
# KEEP APP ALIVE
# ==================================================

keyboard.wait()