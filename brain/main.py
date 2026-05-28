from commands import *

assistant_name = "JARVIS"

# ---------------- MEMORY SYSTEM ---------------- #

try:
    with open("brain/user_name.txt", "r") as file:
        user_name = file.read()

except:
    user_name = input(f"{assistant_name}: I don't know your name yet. What is your name? ")

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
# ---------------- STARTUP ---------------- #

print(f"{assistant_name}: Welcome back, {user_name}.")



# ---------------- MAIN LOOP ---------------- #

while True:

    command = input(f"{assistant_name}: How can I assist you today? ").lower().strip()

    if command == "exit":

        print(f"{assistant_name}: Shutting down.")
        break

    elif command in commands:

        commands[command]()

    else:

        unknown_command(assistant_name)