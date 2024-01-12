from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
import pyperclip
import os
import pickle
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
import json




USER_NAME_AREA = 'input#email' #css
USER_PASS_AREA = 'input#pass' #css
NEW_POST_AREA = '.xi81zsa.x1lkfr7t.xkjl1po.x1mzt3pk.xh8yej3.x13faqbe span.x1lliihq.x6ikm8r.x10wlt62.x1n2onr6' #xpath
TEXT_AREA = '._1mf._1mj' #css
MEDIA_AREA = 'input.x1s85apg:nth-child(1)' #css
SEND_BUTTON_AREA = 'form .x1i10hfl.xjbqb8w.x6umtig.x1b1mbwd.xaqea5y.xav7gou.x1ypdohk.xe8uvvx.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.xexx8yu.x4uap5.x18d9i69.xkhd6sd.x16tdsg8.x1hl2dhg.xggy1nq.x1o1ewxj.x3x9cwd.x1e5q0jg.x13rtm0m.x87ps6o.x1lku1pv.x1a2a7pz.x9f619.x3nfvp2.xdt5ytf.xl56j7k.x1n2onr6.xh8yej3 div div div' #css
COOKIE_BUTTON = '#u_0_k_oM' #css
PHOTO_BUTTON = 'div[aria-label="Фото/видео"]'


class FbBotMain:
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--lang=en")
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_argument("--disable-web-security")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False) 
        chrome_options.add_argument("--disable-features=AutomationControlled")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--disable-audio-output")
        chrome_options.add_argument("--disable-features=AudioServiceOutOfProcess")

        ChromeDriverManager().install()

        self.driver = self.get_chromedriver(chrom_options=chrome_options)
        sleep(2)

    def hz(self):
        pass


    def create_post(self, group, text=None, media_list=None):
        self.driver.get(group)
        sleep(2)
        try:
            self.driver.find_element(By.CSS_SELECTOR, NEW_POST_AREA).click()
        except Exception:
            print('Не нашел кнопку новый пост')
        sleep(5)
        if text is not None:
            try:
                pyperclip.copy(text)
                area = self.driver.find_element(By.CSS_SELECTOR, TEXT_AREA)
                area.click()
                sleep(2)
                area.send_keys(Keys.CONTROL, 'v')
                sleep(3)
            except Exception as e:
                print("не вставил текст", e)
        sleep(1)
        if media_list:
            try:
                for media in media_list:
                    path = media
                    print(path)
                    try:
                        self.driver.find_element(By.CSS_SELECTOR, MEDIA_AREA).send_keys(path)
                    except:
                        try:
                            self.driver.find_element(By.CSS_SELECTOR, PHOTO_BUTTON).click()
                            sleep(2)
                        except:
                            pass
                        self.driver.find_element(By.CSS_SELECTOR, MEDIA_AREA).send_keys(path)
                    sleep(3)
            except Exception as e:
                print("не вставил медиа", e)
        sleep(1)
        try:
            sleep(2)
            self.driver.find_elements(By.CSS_SELECTOR, SEND_BUTTON_AREA)[-1].click()
            return True
        except Exception:
            print('Проблема с кнопкой отправить')
            return False





    def quit_driver(self):
        pickle.dump(self.driver.get_cookies(), open("cookies.pkl", "wb"))
        self.driver.quit()



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
    


    def log_in(self, username, password):
        sleep(3)
        self.driver.get("https://www.facebook.com/")
        sleep(2)
        try:
            self.driver.find_element(By.CSS_SELECTOR, COOKIE_BUTTON).click()
        except Exception as e:
            print(e)
        try:
            sleep(2)
            self.driver.find_element(By.CSS_SELECTOR, USER_NAME_AREA).send_keys(username)
            sleep(2)
            self.driver.find_element(By.CSS_SELECTOR, USER_PASS_AREA).send_keys(password)
            sleep(2)
            self.driver.find_element(By.CSS_SELECTOR, USER_PASS_AREA).send_keys(Keys.ENTER)
            sleep(3)
        except Exception as e:
            print('Не смог войти в акк, нужен перезапуск скрипта', e)
            self.quit_driver()




def main_create_posts(text=None, media_list=None, wait_time=60, all_grps=[]):
    with open("selenium.json", "r") as f:
        saved_settings = json.load(f)
    content = saved_settings['content']
    if content == 'Фото':
        text = None
        media_list = media_list
    elif content == 'Текст':
        text = text
        media_list = None
    elif content == "Фото+Текст":
        text=text
        media_list=media_list
    was_send = 0
    bott = FbBotMain()
    counter = {}
    for group in all_grps:
        with open("selenium.json", "r") as f:
            saved_settings = json.load(f)
        flag = saved_settings['flag']
        if flag:
            break
        result = bott.create_post(group, text, media_list)
        if result == True:
            was_send += 1
            counter['count'] = was_send
            with open("counter.json", "w") as f:
                json.dump(counter, f)
            #self.sent_label['text'] = f"Отправил: {was_send}"
        sleep(int(wait_time))
    bott.quit_driver()
