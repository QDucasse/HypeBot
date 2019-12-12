from hypebot import *
import schedule
import time

def job_test():
    product_name = 'Supreme/dead prez Tee'
    hypettbot = HypeTTPBot(name=product_name,category='new')
    hypettbot.get_item_id()
    hypebot = Hypebot(name=product_name)
    hypebot.add_to_cart(hypettbot.prod_id)
    sleep(0.1)
    hypebot.fill_checkout()

schedule.every().day.at("10:34").do(job_test)

while True:
    schedule.run_pending()
    time.sleep(0.1) # wait one minute
