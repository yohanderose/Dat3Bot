from selenium import webdriver
import time
import random

# TODO: - Store logins and passwords separately 
#       - Sometimes does not show google login method 
#       - Handle popups during swiping

class Bot():
    def __init__(self):
        self.driver = webdriver.Chrome()

    def login(self):
        self.driver.get('https://tinder.com/')
        time.sleep(10)

        # Click to open all options
        #self.driver.find_element_by_xpath('//*[@id="modal-manager"]/div/div/div/div/div[3]/span/button').click()

        # Click login with Google
        try:
            self.driver.find_element_by_xpath('//*[@id="modal-manager"]/div/div/div/div/div[3]/span/div[1]/div/button').click()
            time.sleep(1)
            window_before = self.driver.window_handles[0] 
            window_after = self.driver.window_handles[1]
            
            self.driver.switch_to_window(window_after)
            # email = ''
            # password = ''
            self.driver.find_element_by_xpath('//*[@id="identifierId"]').send_keys(email) 
            self.driver.find_element_by_xpath('//*[@id="identifierNext"]/span').click()
            time.sleep(1)
            self.driver.find_element_by_xpath('//*[@id="password"]/div[1]/div/div[1]/input').send_keys(password)
            self.driver.find_element_by_xpath('//*[@id="passwordNext"]/span/span').click()
            self.driver.switch_to_window(window_before)
            time.sleep(1)
        except Exception as e:
            print("ERROR:\tCould not find login method!!")
        
        # Allow cookies
        self.driver.find_element_by_xpath('//*[@id="content"]/div/div[3]/div/div/div/button/span').click()
        # Allow location services
        self.driver.find_element_by_xpath('//*[@id="modal-manager"]/div/div/div/div/div[3]/button[1]/span').click()
        # Disable notifications
        self.driver.find_element_by_xpath('//*[@id="modal-manager"]/div/div/div/div/div[3]/button[2]/span').click()
        
        # Define swipe buttons
        like = self.driver.find_element_by_xpath('//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div[1]/div[2]/div[4]/button')
        dislike =  self.driver.find_element_by_xpath('//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div[1]/div[2]/div[2]/button')

        while True:
            test = random.random()
            if test > 0.6:
                like.click()
            else:
                dislike.click()
            time.sleep(2)

bot = Bot()
bot.login()