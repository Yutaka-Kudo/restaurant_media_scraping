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

from rq import Queue
from worker import conn



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

    error_flg = False

    driver = webdriver.Chrome(chrome_options=options)
    driver.set_window_size(1250, 1036)
    driver.implicitly_wait(5)

    print('Browser is ready!')

    # In[5]:

    url = "https://www.cms.hotpepper.jp/CLN/login/"
    driver.get(url)

    print('get url!')
    sleep(1)

    # In[8]:
    user_name = "C329569"
    pw = "fes130!!"

    # In[10]:

    # フォーム取得
    id_input = driver.find_element_by_xpath("/html/body/div[2]/div/form/div/div[2]/table/tbody/tr[1]/td/input")
    pw_input = driver.find_element_by_name('password')

    # In[11]:

    # 中身をクリア
    id_input.clear()
    pw_input.clear()

    sleep(1)

    # In[12]:

    try:
        # 入力
        # driver.find_element_by_xpath(
        #     "/html/body/main/div[2]/div/div/div[2]/dl/dd/form/div[3]/div[1]/label").click()
        id_input.send_keys(user_name)
        pw_input.send_keys(pw)
        print('input OK!')
    except Exception:
        error_flg = True
        print('インプットエラー')
    if error_flg is False:
        try:
            pw_input.submit()
            sleep(2)
            print('login OK!')
        except Exception:
            error_flg = True
            print('ログインエラー')

    #店舗選択
    if error_flg is False:
        try:
            elem = driver.find_element_by_link_text('Garage Kitchenあそび　西船橋店')
            elem.click()
            sleep(2)
            print('store select OK!')
        except Exception:
            error_flg = True
            print('店舗選択エラー')
    # In[15]:


        #レポートボタンクリック
    if error_flg is False:
        try:
            report_btn = driver.find_element_by_link_text('アクセス・レポート')
            report_btn.click()
            sleep(2)
            print('report btn click OK!')
        except Exception:
            error_flg = True
            print('レポートボタンクリックエラー')

    handle_array = driver.window_handles
    print(handle_array[0])
    print(handle_array[1])
    # 操作ウィンドウを変更する
    driver.switch_to.window(handle_array[-1])
    sleep(1)
    print('handle OK!')

    # In[16]:

    try:
        df_lists = []
        i = 24  # 20
        while i <= 25:
            # 月選択
            month_select_elem = driver.find_element_by_name('numberCd')
            month_select_object = Select(month_select_elem)
            month_select_object.select_by_index(i)
            sleep(2)

            # ここにデータ取得コードを。
            df_list = pd.read_html(driver.page_source)
            df_lists.append(df_list[4])

            i += 1

    except Exception:
        error_flg = True
        print('データ収集エラー')


    # In[13]:
    df_fix = pd.concat([df_lists[i] for i in range(0, len(df_lists))])
    print('create df_list')

    now = dt.datetime.now().strftime('%Y%m%d')
    oldpath = 'data_garage_hp_sp_{}.csv'.format(now)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename={}'.format(oldpath)
    df_fix.to_csv(path_or_buf=response, sep=';', float_format='%.2f', index=False, decimal=",")

    sleep(2)
    driver.quit()

    return response

def grgHpSp(request):
    q = Queue(connection=conn)
    result = q.enqueue(grg_hp_sp, "request")
    return result