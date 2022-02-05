
from tkinter.messagebox import QUESTION
from xml.dom.minidom import Document
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
chrome_options = Options()
#chrome_options.add_argument("--disable-extensions")
#chrome_options.add_argument("--disable-gpu")
#chrome_options.add_argument("--headless")
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
chrome_options.add_experimental_option("detach", True)
chrome_options.add_argument("--mute-audio")
class client:
    def __init__(self):
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), port=8080, options=chrome_options)
        self.waiting = False

    def launch(self):
        self.driver.implicitly_wait(30)
        self.driver.set_page_load_timeout(50)
    def login(self, username, password):
        self.driver.get('https://create.kahoot.it/auth/login')
        self.driver.implicitly_wait(10)
        self.driver.set_page_load_timeout(30)
        USERBOX = self.driver.find_element_by_id('username')
        PASSBOX = self.driver.find_element_by_id('password')
        LOGBTN = self.driver.find_element_by_id('login-submit-btn')
        USERBOX.send_keys(username)
        PASSBOX.send_keys(password)
        self.driver.execute_script("arguments[0].click();", LOGBTN)
    def Initiate(self, gameUrl):
        self.driver.get(gameUrl)
        self.driver.implicitly_wait(10)
        self.driver.set_page_load_timeout(30)
        GUESTBTN = self.driver.find_element_by_xpath("""//*[@id="sign-in-dialog"]/div/div[3]/a""")
        self.driver.execute_script("arguments[0].click();", GUESTBTN)
        START = self.driver.find_element_by_xpath("""//*[@id="launch"]/div[4]/div[2]/div[1]/button""")
        START.click()
    def fetchInfo(self):
        print('Getting Info..')
        #waiting for pin
        pin = self.driver.find_element_by_xpath('//*[@id="theme-scroll-wrapper"]/div/main/div[4]/div[2]/div/div[1]/div/div[2]/div/div/div/div[2]/div/div/button')
        self.driver.get_screenshot_as_file("Assets/PIN.png")
        self.link = 'https://kahoot.it/?pin=' + pin.text + '&refer_method=link'
    def checkPlayerJoin(self):
        self.driver.implicitly_wait(120)
        player = self.driver.find_element_by_xpath('//*[@id="theme-scroll-wrapper"]/div/main/section/ul/li/button/span')
        return player
    def getQuestion(self):
        print('Getting question')
        self.question = self.driver.find_element_by_xpath(
            '//*[@id="theme-scroll-wrapper"]/div/main/div[1]/section/div[1]/section')
        self.driver.get_screenshot_as_file(".\Assets\Question.png")
        

    def startGame(self):
        STARTBTN = self.driver.find_element_by_class_name('sc-gsDrkp hazGmN')
        self.driver.execute_script("arguments[0].click();", STARTBTN)