from bot import Bot
from getpass import getpass

def main():
    email = input("Email: ")
    password = getpass("Password: ")

    print("Initialising bot...")
    bot = Bot()
    bot.login(email, password)

if __name__ == "__main__":
    main()