from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# import chromedriver_binary
from time import sleep
import pandas as pd
import datetime as dt
# import itertools
# import os
import random
from django.http import HttpResponse, HttpResponseRedirect

# from django.shortcuts import render
# from .models import Scraping
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.urls import reverse
import os


def grg_hp_sp(request):
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
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')  # 不要？?
    options.add_argument('--disable-desktop-notifications')
    options.add_argument("--disable-extensions")
    options.add_argument('--lang=ja')
    options.add_argument('--blink-settings=imagesEnabled=false')  # 画像なし
    options.add_argument('--no-sandbox')
    # options.binary_location = '/usr/bin/google-chrome'
    options.add_argument('--proxy-bypass-list=*')      # すべてのホスト名
    options.add_argument('--proxy-server="direct://"')  # Proxy経由ではなく直接接続する
    # if chrome_binary_path:
    #     options.binary_location = chrome_binary_path
    options.add_argument('--single-process')
    # options.add_argument('--disable-application-cache')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--start-maximized')

    error_flg = False

    driver = webdriver.Chrome(chrome_options=options)
    driver.set_window_size(1250, 1036)
    driver.implicitly_wait(5)
    print('Browser is ready!')

    # In[5]:

    url = "https://www.cms.hotpepper.jp/CLN/login/"
    driver.get(url)
    print('get url!')
    # In[8]:

    sleep(1)
    download_dir = "static/temp/"
    # os.mkdir(download_dir)
    driver.save_screenshot(download_dir + 'result.png')
 
    # In[9]:
    print('save screenshot')
    
    driver.quit()
    return redirect("/")

    # df_fix.to_csv(oldpath, mode="x", encoding="utf_8_sig")

    # file = Scraping()
