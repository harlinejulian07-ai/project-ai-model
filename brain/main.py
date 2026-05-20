assistant_name = "JARVIS"

try:
    with open("brain/user_name.txt", "r") as file:
        user_name = file.read()

    print(f"{assistant_name}: Welcome back, {user_name}.")

except:
    user_name = input("JARVIS: I don't know your name yet. What is your name? ")

    with open("brain/user_name.txt", "w") as file:
        file.write(user_name)

    print(f"{assistant_name}: Nice to meet you, {user_name}.")