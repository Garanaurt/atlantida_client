from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium import webdriver
from time import sleep
from selenium.webdriver.chrome.options import Options
import pickle



class FbBot:
    def __init__(self):
        self.chrome_options = Options()
        self.chrome_options.add_argument("--lang=en")
        self.chrome_options.add_argument("--start-maximized")
        self.chrome_options.add_argument("--no-sandbox")
        self.chrome_options.add_argument("--disable-infobars")
        self.chrome_options.add_argument("--disable-web-security")
        self.chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        self.chrome_options.add_experimental_option('useAutomationExtension', False) 
        self.chrome_options.add_argument("--disable-features=AutomationControlled")
        self.chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        self.chrome_options.add_argument("--disable-notifications")

        ChromeDriverManager().install()
        
        self.driver = self.get_chromedriver(chrom_options=self.chrome_options)
        sleep(2)
        self.log_in()



    def quit_driver(self):
        name = self.driver.find_elements(By.CSS_SELECTOR, 'span.x1lliihq.x6ikm8r.x10wlt62.x1n2onr6')
        account = name[0].text
        pickle.dump(self.driver.get_cookies(), open("cookies.pkl", "wb"))
        self.driver.quit()
        return account



    def get_chromedriver(self, chrom_options=None):
        chrome_options = chrom_options
        driver = webdriver.Chrome(options=chrome_options)
        try:
            cookies = pickle.load(open("cookies.pkl", "rb"))
            driver.get("https://facebook.com")
            sleep(1)
            for cookie in cookies:
                driver.add_cookie(cookie)
            print('kuki ok')
        except Exception as e:
            print(e)
        return driver
    


    def log_in(self):
        self.driver.get("https://www.facebook.com/")

#bot = FbBot()