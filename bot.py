import undetected_chromedriver.v2 as uc
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium import webdriver
import time
import random


#   TODO:
#       - Create AI to simulate my attraction preferences when swiping
#       - Provide support for Bumble and others services
#       - Sometimes the google login option isn't available
#       - Test on Linux
#       - Make demo video

LOGIN_XPATH = '//*[@id="q554704800"]/div/div[1]/div/div/main/div/div[2]/div/div[3]/div/div/button[2]'
GOOGLE_XPATH = '//*[@id="q-1173676276"]/div/div/div[1]/div/div/div[3]/span/div[1]/div/button'


class Bot():
    def __init__(self):
        capabilities = DesiredCapabilities().CHROME

        chrome_options = uc.ChromeOptions()
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--lang=en-GB")

        prefs = {
            'profile.default_content_setting_values':
            {
                'notifications': 0,
                'geolocation': 1
            },

            'profile.managed_default_content_settings':
            {
                'geolocation': 1
            },
        }

        chrome_options.add_experimental_option('prefs', prefs)
        capabilities.update(chrome_options.to_capabilities())
        self.driver = uc.Chrome(options=chrome_options)

    def login(self, email, password):
        self.driver.get('https://tinder.com/')
        time.sleep(2)

        try:
            # Decline trackers and cookies
            self.driver.find_element(
                By.XPATH, '//*[@id="q554704800"]/div/div[2]/div/div/div[1]/div[1]/button').click()
        except Exception as e:
            print('No Cookie prompt found')
        time.sleep(2)

        self.login_button = None
        self.google_login_button = None

        try:
            self.login_button = self.driver.find_element(By.XPATH,
                                                         '//*[@id="q554704800"]/div/div[1]/div/div/main/div/div[2]/div/div[3]/div/div/button[2]')
            self.login_button.click()
            time.sleep(2)
            self.google_login_button = self.driver.find_element(By.CSS_SELECTOR,
                                                                '[aria-label="Log in with Google"]')
            self.google_login_button.click()
        except Exception as e:
            print("Couldn't open login portal... Trying again")
            time.sleep(2)
            self.google_login_button.click()
            time.sleep(2)
            self.google_login_button.click()

        try:

            window_before = self.driver.window_handles[0]
            window_after = self.driver.window_handles[1]
            self.driver.switch_to.window(window_after)

            self.driver.find_element(By.XPATH,
                                     '//*[@id="identifierId"]').send_keys(email)
            self.driver.find_element(By.XPATH,
                                     '//*[@id="identifierNext"]/div/button').click()
            time.sleep(2)

            self.driver.find_element(By.XPATH,
                                     '//*[@id="password"]/div[1]/div/div[1]/input').send_keys(password)
            self.driver.find_element(By.XPATH,
                                     '//*[@id="passwordNext"]/div/button').click()

            wait = input('Log in, and press enter to continue...')

            self.driver.switch_to.window(window_before)
        except Exception as e:
            print("ERROR:\t Couldn't login with credentials.")

    def run(self):
        pass
        # Allow location services
        try:
            self.driver.find_element(
                By.CSS_SELECTOR, '[aria-label="Allow"]').click()
        except Exception as e:
            print("ERROR:\t Couldn't allow location services.")
        time.sleep(2)

        # Disable notifications
        try:
            self.driver.find_element(
                By.CSS_SELECTOR, '[aria-label="Not interested"]').click()
        except Exception as e:
            print("ERROR:\t Couldn't disable notifications.")

        time.sleep(3)

        self.like = None
        self.dislike = None
        # Define swipe buttons
        try:
            self.like = self.driver.find_element(By.XPATH,
                                                 '//*[@id="q554704800"]/div/div[1]/div/div/main/div/div/div/div/div[4]/div/div[4]/button')
            self.dislike = self.driver.find_element(By.XPATH,
                                                    '//*[@id="q554704800"]/div/div[1]/div/div/main/div/div/div/div/div[4]/div/div[2]/button')
        except Exception as e:
            print("ERROR:\t Couldn't assign like or dislike buttons.")

        # while True:
        #     time.sleep(1)
        #     # Check for popups
        #     try:
        #         self.driver.find_element_by_xpath(
        #             '//*[@id="modal-manager"]/div/div/div[2]/button[2]/span').click()
        #         print("ALERT:\t Dealt with home screen popup.")
        #     except Exception as e:
        #         pass

        #     time.sleep(1)

        #     test = random.random()
        #     if test > 0.6:
        #         like.click()
        #     else:
        #         dislike.click()
