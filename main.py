from bot import Bot
# from getpass import getpass
from credentials import email, pwd


# email = input("Email: ")
# password = getpass("Password: ")
password = pwd

print("Initialising bot...")
bot = Bot()
bot.login(email, password)
