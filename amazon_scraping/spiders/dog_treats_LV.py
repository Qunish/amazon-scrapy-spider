import scrapy
from selenium.webdriver.common.by import By
from ..items import AmazonScrapingItem
import pymongo
import random

DRIVER_FILE_PATH = "/Users/qunishdash/Documents/chromedriver_mac64/chromedriver"
USER_AGENT_LIST = ['Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36',
                    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:86.0) Gecko/20100101 Firefox/86.0',
                    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:72.0) Gecko/20100101 Firefox/72.0',
                    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36',
                    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36'
                    ]

class DogTreatsLvSpider(scrapy.Spider):
    name = "dog_treats_LV"
    handle_httpstatus_list = [403, 503]
    start_urls = [
        "https://www.amazon.com/s?k=dog+treats&rh=n%3A2975434011&ref=nb_sb_noss"
        ]
    
    # def __init__(self):
    #     self.conn = pymongo.MongoClient(
    #         "localhost",
    #         27017
    #     )
    #     db = self.conn["amazon_scrapy_db"]
    #     self.collection = db["dog_treats_lv"]

    def get_chrome_driver(self, headless_flag):
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        if headless_flag:
            # in case you want headless browser
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--disable-extensions")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--start-maximized")
            # chrome_options.add_experimental_option('prefs', {'headers': headers}) # if you want to add custom header
            chrome_options.add_argument("user-agent={}".format(random.choice(USER_AGENT_LIST)))
            driver = webdriver.Chrome(options=chrome_options) 
        else:
            # in case  you want to open browser
            chrome_options = Options()
            # chrome_options.add_experimental_option('prefs', {'headers': headers}) # if you want to add custom header
            chrome_options.add_argument("--start-maximized")
            chrome_options.add_argument("user-agent={}".format(random.choice(USER_AGENT_LIST)))
            chrome_options.headless = False
            driver = webdriver.Chrome(options=chrome_options)

        return driver

    def parse(self, response):
        if response.status == 403:
            self.logger.warning("Status 403 - but chill we are handling using selenium driver.")

        driver = self.get_chrome_driver(headless_flag=False)
        driver.get(response.url)

        items = AmazonScrapingItem()

        all_cards = driver.find_elements(By.CSS_SELECTOR, ".s-card-border")
        for card in all_cards:
            try:
                name = card.find_element(By.XPATH, "/html/body/div[1]/div[2]/div[1]/div[1]/div/span[1]/div[1]/div/div/div//div[2]/div/h2").text
            except Exception as e:
                name = ''
            # try:
            #     type_of_property = card.find_element(By.CSS_SELECTOR, "").text
            # except Exception as e:
            #     type_of_property = ''
            # try:
            #     number_of_bedrooms = card.find_element(By.CSS_SELECTOR, ".kkHNg .qkjPI").text
            # except Exception as e:
            #     number_of_bedrooms = ''
            # try:
            #     number_of_bathrooms = card.find_element(By.CSS_SELECTOR, ".WIPQs .qkjPI").text
            # except Exception as e:
            #     number_of_bathrooms = ''
        # name = response.css(".a-color-base.a-text-normal::text").extract()
        # no_of_review = response.css(".s-link-style .s-underline-text::text").extract()
        
        items["name"] = name

        yield items

        driver.quit()
