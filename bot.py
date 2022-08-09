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
        self.driver = webdriver.Chrome()

    def login(self, email, password):
        self.driver.get('https://tinder.com/')
        time.sleep(2)

        try:
            # Decline trackers and cookies
            self.driver.find_element_by_xpath(
                '//*[@id="q554704800"]/div/div[2]/div/div/div[1]/div[2]/button').click()
            # Try login with Google
            self.driver.find_element_by_xpath(
                '//*[@id="q554704800"]/div/div[1]/div/div/main/div/div[2]/div/div[3]/div/div/button[2]').click()
            time.sleep(2)
            self.driver.find_element_by_xpath(
                '//*[@id="q-1173676276"]/div/div/div[1]/div/div/div[3]/span/div[1]/div/button').click()

            time.sleep(1)
            window_before = self.driver.window_handles[0]
            window_after = self.driver.window_handles[1]

            self.driver.switch_to.window(window_after)
            self.driver.find_element_by_xpath(
                '//*[@id="identifierId"]').send_keys(email)
            self.driver.find_element_by_xpath(
                '//*[@id="identifierNext"]/span').click()
            time.sleep(2)
            self.driver.find_element_by_xpath(
                '//*[@id="password"]/div[1]/div/div[1]/input').send_keys(password)
            self.driver.find_element_by_xpath(
                '//*[@id="passwordNext"]/span/span').click()
            self.driver.switch_to.window(window_before)
        except Exception as e:
            print("ERROR:\tCould not find login method!!")

        # time.sleep(3)

        # # Allow cookies
        # try:
        #     self.driver.find_element_by_xpath(
        #         '//*[@id="content"]/div/div[3]/div/div/div/button/span').click()
        # except Exception as e:
        #     print("ERROR:\t Couldn't allow cookies.")

        # time.sleep(2)

        # # Allow location services
        # try:
        #     self.driver.find_element_by_xpath(
        #         '//*[@id="modal-manager"]/div/div/div/div/div[3]/button[1]/span').click()
        # except Exception as e:
        #     print("ERROR:\t Couldn't allow location services.")

        # time.sleep(2)

        # # Disable notifications
        # try:
        #     self.driver.find_element_by_xpath(
        #         '//*[@id="modal-manager"]/div/div/div/div/div[3]/button[2]/span').click()
        # except Exception as e:
        #     print("ERROR:\t Couldn't disable notifications.")

        # time.sleep(2)

        # # Define swipe buttons
        # try:
        #     like = self.driver.find_element_by_xpath(
        #         '//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div[1]/div[2]/div[4]/button')
        #     dislike = self.driver.find_element_by_xpath(
        #         '//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div[1]/div[2]/div[2]/button')
        # except Exception as e:
        #     print("ERROR:\t Couldn't assign like or dislike buttons.")

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
