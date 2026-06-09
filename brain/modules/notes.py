import os
import subprocess

# ==================================================
# PATHS
# ==================================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

NOTES_FILE = os.path.join(
    BASE_DIR,
    "..",
    "..",
    "notes",
    "notes.txt"
)

# ==================================================
# HELPERS
# ==================================================

def ensure_notes_folder():

    os.makedirs(
        os.path.dirname(NOTES_FILE),
        exist_ok=True
    )

# ==================================================
# OPEN NOTES
# ==================================================

def open_notes():

    ensure_notes_folder()

    if not os.path.exists(NOTES_FILE):

        with open(
            NOTES_FILE,
            "w",
            encoding="utf-8"
        ):
            pass

    subprocess.Popen(
        ["notepad.exe", NOTES_FILE]
    )

# ==================================================
# SAVE NOTE
# ==================================================

def save_note(note_text):

    ensure_notes_folder()

    with open(
        NOTES_FILE,
        "a",
        encoding="utf-8"
    ) as file:

        file.write(note_text + "\n")

# ==================================================
# GET NOTES
# ==================================================

def get_notes():

    ensure_notes_folder()

    try:

        with open(
            NOTES_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            return file.readlines()

    except FileNotFoundError:

        return []

# ==================================================
# CLEAR NOTES
# ==================================================

def clear_notes():

    ensure_notes_folder()

    with open(
        NOTES_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        file.write("")