from commands import *

from pystray import Icon, MenuItem, Menu
from PIL import Image, ImageDraw

import threading
import os
import time

# ---------------- CONFIG ---------------- #

assistant_name = "JARVIS"

# ---------------- MEMORY SYSTEM ---------------- #

try:

    with open("brain/user_name.txt", "r") as file:
        user_name = file.read().strip()

except FileNotFoundError:

    user_name = input(
        f"{assistant_name}: I don't know your name yet. What is your name? "
    )

    with open("brain/user_name.txt", "w") as file:
        file.write(user_name)

# ---------------- COMMAND ROUTER ---------------- #

commands = {

    "hello": lambda: greet_user(assistant_name, user_name),

    "time": lambda: tell_time(assistant_name),

    "how are you": lambda: system_status(assistant_name),

    "youtube": lambda: open_youtube(assistant_name),

    "google": lambda: open_google(assistant_name),

    "notepad": lambda: open_notepad(assistant_name),

    "note": lambda: save_note(assistant_name),

    "show notes": lambda: show_notes(assistant_name),

    "clear notes": lambda: clear_notes(assistant_name)
}

# ---------------- STARTUP SEQUENCE ---------------- #

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

print(f"{assistant_name}: Welcome back, {user_name}.")

# ---------------- BACKGROUND REMINDER THREAD ---------------- #

reminder_thread = threading.Thread(
    target=hourly_reminder_loop,
    args=(assistant_name,),
    daemon=True
)

reminder_thread.start()

# ---------------- SYSTEM TRAY ---------------- #

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

    print("JARVIS shutting down.")

    icon.stop()

    os._exit(0)


def setup_tray():

    tray_icon = Icon(
        "JARVIS",
        create_image(),
        "JARVIS Assistant",
        menu=Menu(
            MenuItem("Quit", quit_jarvis)
        )
    )

    tray_icon.run()


tray_thread = threading.Thread(
    target=setup_tray,
    daemon=True
)

tray_thread.start()

# ---------------- MAIN LOOP ---------------- #

while True:

    command = input(
        f"{assistant_name}: How can I assist you today? "
    ).lower().strip()

    if command == "exit":

        print(f"{assistant_name}: Shutting down.")

        break

    elif command in commands:

        commands[command]()

    else:

        unknown_command(assistant_name)