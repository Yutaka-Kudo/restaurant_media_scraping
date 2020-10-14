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


def index(request):
    return render(request, "scr/index.html")

# class Index(TemplateView):
#     template_name = "scr/index.html"


def garage(request):
    return render(request, "scr/garage.html")
# class Garage(TemplateView):
#     template_name = "scr/garage.html"


def grg_gn_sp(request):
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
    options.add_argument('--disable-application-cache')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--start-maximized')


    error_flg = False

    driver = webdriver.Chrome(chrome_options=options)
    driver.implicitly_wait(5)

    # In[5]:

    url = "https://pro.gnavi.co.jp/"
    driver.get(url)

    # In[8]:

    sleep(1)

    # In[9]:

    user_name = "ga42902"
    pw = "45675678"

    # In[10]:

    # フォーム取得
    id_input = driver.find_element_by_id("loginID")
    pw_input = driver.find_element_by_id('input_password')

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
    except Exception:
        error_flg = True
        print('インプットエラー')

    # In[13]:

    if error_flg is False:
        try:
            pw_input.submit()
            sleep(2)
        except Exception:
            error_flg = True
            print('ログインエラー')

    # In[14]:

    if error_flg is False:
        try:
            # elem = WebDriverWait(driver, 20).until(EC.element_to_be_clickable(
            #     (By.XPATH, '/html/body/center/div/div[3]/div[1]/div[1]/input')))
            # elem.click()
            driver.find_element_by_xpath('/html/body/center/div/div[3]/div[1]/div[1]/input').click()
            sleep(2)
        except Exception:
            error_flg = True
            print('エラー')

    # In[15]:

    # 未確認情報存在時
    try:
        elem = driver.find_element_by_id('js-unconfirmedRsvModalClose')
        elem.click()
        sleep(2)
    except Exception:
        pass

    # GONアクセス集計　クリック
    if error_flg is False:
        try:
            elem = WebDriverWait(driver, 20).until(EC.element_to_be_clickable(
                (By.XPATH, '//input[@value="アクセス状況の詳細を確認"]')))
            elem.click()
            sleep(2)
        except Exception:
            error_flg = True
            print('エラー GONアクセス集計　クリック時')

    # # ↑別のやり方
    # elem = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH,'//input[@value="アクセス状況の詳細を確認"]')))

    # In[16]:

    # PC　クリック
    if error_flg is False:
        try:
            driver.find_element_by_xpath("//a[text()='PC']").click()
            sleep(2)
        except Exception:
            error_flg = True
            print('エラー　PCクリック時')

    # In[17]:

    # 本番用
    # if error_flg is False:
    try:
        df_lists = []
        # i = 1
        # while i >= 0:
        #     # 月選択
        #     month_select_elem = driver.find_element_by_id('ym')
        #     month_select_object = Select(month_select_elem)
        #     month_select_object.select_by_index(i)
        #     sleep(2)

            # ここにデータ取得コードを。
        df_list = pd.read_html(driver.page_source)
        df_lists.append(df_list[0])

            # i -= 1

    except Exception:
        error_flg = True
        print('エラー')

    # In[18]:
    driver.close()

    now = dt.datetime.now().strftime('%Y%m%d')

    # In[19]:

    df_list_fix = []
    for df in df_lists:
        df.columns = ['日にち', "天気", "合計", '店舗トップ', 'メニュー',
                      '席・個室・貸切', '写真', 'こだわり', '地図', 'クーポン', '予約', 'その他']
        df.drop('天気', axis=1, inplace=True)
        # df.drop(df.index[list(range(len(df)-3,len(df)))],inplace=True)
        # どちらでも可
        df.drop(df.tail(3).index, inplace=True)
        df.set_index('日にち', inplace=True)
        df.index = df.index.str.rstrip('(月火水木金土日)')
        df.index = pd.to_datetime(df.index, format='%Y/%m/%d')
        df.insert(0, "曜日", df.index.strftime('%a'))
        df['曜日'].replace({
            "Mon": "月",
            "Tue": "火",
            "Wed": "水",
            "Thu": "木",
            "Fri": "金",
            "Sat": "土",
            "Sun": "日"
        }, inplace=True)

        df_list_fix.append(df)

    # In[20]:

    df_fix = pd.concat([df_list_fix[i] for i in range(0, len(df_list_fix))])

    # In[56]:

    oldpath = './data_grg_gn_{}.csv'.format(now)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename={}'.format(oldpath)
    df_fix.to_csv(path_or_buf=response, sep=';', float_format='%.2f', index=False, decimal=",")
    return response
    # return render(request, "scr/index.html")

    # df_fix.to_csv(oldpath, mode="x", encoding="utf_8_sig")

    # file = Scraping()
