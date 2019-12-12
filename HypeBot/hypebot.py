import os
import time
import requests

from time     import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options




# chrome_options.add_argument("--disable-extensions")
# chrome_options.add_argument("--disable-gpu")
# chrome_options.add_argument("--headless")

start_time = time.time()

## URLS & HEADERS
## ==============

base_url  = 'https://www.supremenewyork.com/'
url_stock = 'https://www.supremenewyork.com/mobile_stock.json'
url_capt  = 'http://localhost:3001/fetch'
headers_mobile = {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5376e Safari/8536.25', 'Content-type': 'application/x-www-form-urlencoded'}

## CHECKOUT INFORMATION
## ====================

name = 'Testi Boi'
email = 'testiboi@gmail.com'
tel = '0011223344'
address = '11 McDonalds Street'
city = 'Test'
zip_code = '99999'
country = 'FRANCE'

cc_type = 'Visa'
cc_num = '1234 5678 1234 5678'
cc_month = '11'
cc_year = '2021'
cc_cvv = '999'


class HypeTTPBot():
    def __init__(self,name,style=None,size='Medium',category='new'):
        self.prod_name  = name
        self.prod_size  = size
        self.prod_style = style
        self.prod_cat   = category
        self.prod_id    = 0
        self.prod_siid  = 0
        self.prod_stid  = 0

    def get_item_id(self,category=None,name=None):
        '''
        Get the item id from its name and category.
        '''
        if category is None:
            category=self.prod_cat
        if name is None:
            name=self.prod_name
        # Request the mobile_stock.json with a mobile user agent
        r = requests.get(url_stock, headers=headers_mobile)
        base_dict = r.json()
        # Take the dictionary of the products of a given category
        items_from_cat = base_dict['products_and_categories'][category]
        # Iterates through the items of the category
        for item in items_from_cat:
            if item['name'] ==  name:
                id = item['id']
                self.prod_id = id
                return(id)

    def get_new_item_id(self,name=None):
        '''
        Get a new item id (will look in the 'new' category).
        '''
        if name is None:
            name=self.prod_name
        # Uses the category "new"
        get_item_id(category='new',name=name)

    def get_style_size_ids(self,product_id=None,product_style=None,product_size=None):
        '''
        Get the style and size id using the wanted size, style and item id.
        '''
        if product_id is None:
            product_id=self.prod_id
        if product_style is None:
            product_style=self.prod_style
        if product_size is None:
            product_size=self.prod_size
        # Creates the url of the product to access styles/sizes
        url_product = 'https://www.supremenewyork.com/shop/{}.json'.format(product_id)
        r = requests.get(url_product, headers=headers_mobile)
        styles = r.json()['styles']
        style_id = 0
        size_id = 0

        # Iterates through the different styles
        for style in styles:
            if style['name'] == product_style:
                style_id = style['id']
                self.prod_stid = style_id
                sizes = style['sizes']

                # Iterates throught the sizes
                for size in sizes:
                    if size['name'] == product_size:
                        size_id = size['id']
                        self.prod_siid = size_id


        return size_id, style_id

    def get_cookies(self):
        r = requests.get(url_capt)
        return r.json()


    def add_to_cart(item_id, size_id, style_id):
        '''
        Add to cart (POST request with the style and size id parameters) and output the produced cookies.
        '''
        if item_id is None:
            item_id = self.prod_id
        if size_id is None:
            size_id = self.prod_siid
        if style_id is None:
            style_id = self.prod_stid
        payload = {"size": size_id, "style": style_id, "qty": '1'}
        url_product = 'https://www.supremenewyork.com/shop/{}/add.json'.format(item_id)
        r = requests.post(url_product, params=payload, ) # headers=headers_mobile
        return dict(r.cookies)


class Hypebot:
    def __init__(self,name,style=None,size=None,category='new'):
        chrome_options = Options()
        # mobile_emulation = {
        #     "deviceMetrics": { "width": 360, "height": 640, "pixelRatio": 3.0 },
        #     "userAgent": "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19"
        # }
        # chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
        self.driver = webdriver.Chrome(executable_path=os.path.abspath("./drivers/chromedriver"), options=chrome_options)

    def close_browser(self):
        self.driver.close()

    def add_to_cart(self,prod_id):
        url_product='https://www.supremenewyork.com/shop/'+str(prod_id)
        self.driver.get(url_product)
        self.driver.find_element_by_xpath("""//*[@id="add-remove-buttons"]/input""").click()

    def fill_checkout(self):
        # Address info
        self.driver.find_element_by_xpath("""//*[@id="cart"]/a[2]""").click()
        self.driver.execute_script("document.getElementById('order_billing_name').setAttribute('value','{}');".format(name))
        self.driver.execute_script("document.getElementById('order_email').setAttribute('value','{}');".format(email))
        self.driver.execute_script("document.getElementById('order_tel').setAttribute('value','{}');".format(tel))
        self.driver.execute_script("document.getElementById('bo').setAttribute('value','{}');".format(address))
        self.driver.execute_script("document.getElementById('order_billing_zip').setAttribute('value','{}');".format(zip_code))
        self.driver.execute_script("document.getElementById('order_billing_city').setAttribute('value','{}');".format(city))
        self.driver.execute_script("document.getElementById('order_billing_country').setAttribute('value','{}');".format(country))
        # Credit card info
        self.driver.execute_script("document.getElementById('credit_card_type').setAttribute('value','{}');".format(cc_type))
        self.driver.execute_script("document.getElementById('cnb').setAttribute('value','{}');".format(cc_num))
        self.driver.execute_script("document.getElementById('credit_card_month').setAttribute('value','{}');".format(cc_month))
        self.driver.execute_script("document.getElementById('credit_card_year').setAttribute('value','{}');".format(cc_year))
        self.driver.execute_script("document.getElementById('vval').setAttribute('value','{}');".format(cc_cvv))
        # Captcha
        # captcha_token = self.httpbot.get_cookies()[0]['token']
        # self.driver.execute_script("document.getElementById('g-recaptcha-response').setAttribute('value','{}');".format(captcha_token))

        # Submit
        self.driver.find_element_by_xpath('//*[@id="cart-cc"]/fieldset/p/label/div/ins').click()
        self.driver.find_element_by_xpath('//*[@id="pay"]/input').click()

    def captcha(self):
        captcha_entry = self.driver.execute_script("document.getElementById('g-recaptcha-response').setAttribute('value','{}');".format(input('enter captcha')))

    def add_cookies(self):
        cookies_list = self.httpbot.get_cookies()
        if len(cookies_list)==0:
            print("Please run Captcha Harvester")
            return
        print(cookies_list)
        first_cookie = cookies_list[0]
        for k, v in zip(list(first_cookie.keys()), list(first_cookie.values())):
            self.driver.add_cookie({'name': k, 'value': v})


class MobileHypebot(Hypebot):
    def __init__(self,*args,**kwargs):
        chrome_options = Options()
        mobile_emulation = {
            "deviceMetrics": { "width": 360, "height": 640, "pixelRatio": 3.0 },
            "userAgent": "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19"
        }
        chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
        self.driver = webdriver.Chrome(executable_path=os.path.abspath("./drivers/chromedriver"), options=chrome_options)

    def add_to_cart(self,prod_id,style_id):
        url_product='https://www.supremenewyork.com/mobile/#products/'+str(prod_id)+'/'+str(style_id)
        self.driver.get(url_product)
        sleep(0.1)
        self.driver.find_element_by_class_name("cart_button").click()
        sleep(1)
        self.driver.find_element_by_xpath("""//*[@id="cart"]/a[2]""").click()


if __name__ == '__main__':
    # product_name  = 'Bandana Box Logo Hooded Sweatshirt'
    # product_size  = 'Medium'
    # product_style = 'Pink'

    product_name  = 'Stripe Shirt'
    product_size  = 'Medium'
    product_style = 'Black'

    # PURE HTTP
    # ==========
    hypettbot = HypeTTPBot(name=product_name,size=product_size,style=product_style,category='Shirts')
    hypettbot.get_item_id()
    print(hypettbot.prod_id)
    hypettbot.get_style_size_ids()
    print(hypettbot.prod_siid)
    print(hypettbot.prod_stid)
    # cookies = add_to_cart(product_id, product_siid, product_stid)
    # print(cookies)

    # HYPEBOT
    # =======
    hypebot = Hypebot(name=product_name,style=product_style,size=product_size)
    hypebot.add_to_cart(hypettbot.prod_id,hypettbot.prod_stid)
    hypebot.fill_checkout()
    sleep(3)
    hypebot.close_browser()

    # MOBHYPEBOT
    # ==========
    # hypebot = MobileHypebot(name=product_name,style=product_style,size=product_size)
    # hypebot.add_to_cart(hypettbot.prod_id,hypettbot.prod_stid)
    # hypebot.fill_checkout()
    # sleep(3)
    # hypebot.close_browser()
