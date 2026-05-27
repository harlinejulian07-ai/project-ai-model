import datetime

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
    print(f"{assistant_name}: Hello, {user_name}.")

def tell_time():
    current_time = datetime.datetime.now().strftime("%I:%M %p")

    print(f"{assistant_name}: The current time is {current_time}.")

def system_status():
    print(f"{assistant_name}: Systems operating normally.")

def unknown_command():
    print(f"{assistant_name}: I do not recognize that command.")

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

# ---------------- MAIN LOOP ---------------- #

while True:

    command = input(f"{assistant_name}: How can I assist you today? ").lower().strip()

    if command == "hello":
        greet_user()

    elif command == "time":
        tell_time()

    elif command == "how are you":
        system_status()

    elif command == "note":
        save_note()

    elif command == "show notes":
        show_notes()

    elif command == "clear notes":
        clear_notes()

    elif command == "exit":
        print(f"{assistant_name}: Shutting down.")
        break

    else:
        unknown_command()