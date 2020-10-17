from selenium import webdriver
# import chromedriver_binary
# import itertools
# import os
import random

user_agent = [
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.2 Safari/605.1.15',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1 Safari/605.1.15',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'
]
options = webdriver.ChromeOptions()
now_ua = user_agent[random.randrange(0, len(user_agent), 1)]
options.add_argument('--user-agent=' + now_ua)
options.add_argument('--disable-desktop-notifications')
options.add_argument("--disable-extensions")
options.add_argument('--lang=ja')
options.add_argument('--blink-settings=imagesEnabled=false')  # 画像なし
# options.add_argument('--no-sandbox')
# options.binary_location = '/usr/bin/google-chrome'
options.add_argument('--proxy-bypass-list=*')      # すべてのホスト名
options.add_argument('--proxy-server="direct://"')  # Proxy経由ではなく直接接続する
# if chrome_binary_path:
#     options.binary_location = chrome_binary_path
# options.add_argument('--single-process')
# options.add_argument('--disable-application-cache')
options.add_argument('--ignore-certificate-errors')
# options.add_argument('--start-maximized')

# options.add_argument('--headless')  # ヘッドレス
# options.add_argument('--disable-gpu')  # 不要？?
