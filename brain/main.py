import datetime

assistant_name = "JARVIS"

try:
    with open("brain/user_name.txt", "r") as file:
        user_name = file.read()

except:
    user_name = input("JARVIS: I don't know your name yet. What is your name? ")

    with open("brain/user_name.txt", "w") as file:
        file.write(user_name)

print(f"{assistant_name}: Welcome back, {user_name}.")

while True:

    command = input(f"{assistant_name}: How can I assist you today? ")

    if command == "hello":
        print(f"{assistant_name}: Hello, {user_name}.")

    elif command == "time":
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        print(f"{assistant_name}: The current time is {current_time}.")

    elif command == "how are you":
        print(f"{assistant_name}: Systems operating normally.")

    elif command == "exit":
        print(f"{assistant_name}: Shutting down.")
        break

    else:
        print(f"{assistant_name}: I do not recognize that command.")
    