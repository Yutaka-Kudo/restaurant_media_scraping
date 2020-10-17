from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# import chromedriver_binary
from time import sleep
import pandas as pd
import datetime as dt
# import itertools
# import os

from django.http import HttpResponse, HttpResponseRedirect
# from django.shortcuts import render, redirect
# from django.views.generic import TemplateView
# from django.urls import reverse

# from .models import Scraping
# import os

# from rq import Queue
# from worker import conn

# from .driver_settings import options

import random


def grg_tb_sp(request):

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

    options.add_argument('--headless')  # ヘッドレス
    options.add_argument('--disable-gpu')  # 不要？?

    error_flg = False
    driver = webdriver.Chrome(chrome_options=options)
    # driver.set_window_size(1250, 1036)
    driver.implicitly_wait(5)

    print('Browser is ready!')

    url = "https://ssl.tabelog.com/owner_account/login/"
    driver.get(url)

    print('get url!')
    # sleep(1)

    user_name = "brguav"
    pw = "Questa130"

    # フォーム取得
    id_input = driver.find_element_by_id('login_id')
    pw_input = driver.find_element_by_id('password')

    # 中身をクリア
    id_input.clear()
    pw_input.clear()

    sleep(1)

    try:
        # 入力
        id_input.send_keys(user_name)
        pw_input.send_keys(pw)
        print('input OK!')
    except Exception:
        error_flg = True
        print('インプットエラー')

    if error_flg is False:
        try:
            pw_input.submit()
            sleep(1)
            print('login OK!')
        except Exception:
            error_flg = True
            print('ログインエラー')

    # 店舗選択
    if error_flg is False:
        try:
            elem = driver.find_element(
                By.XPATH, ("/html/body/div[4]/div[2]/ul/li[4]/div[2]/form/input[4]"))
            elem.click()
            sleep(1)
            print('store select OK!')
        except Exception:
            error_flg = True
            print('店舗選択エラー')

    # アクセス解析クリック
    if error_flg is False:
        try:
            report_btn = driver.find_element_by_link_text('アクセス解析')
            report_btn.click()
            sleep(1)
            print('アクセス解析 btn click OK!')
        except Exception:
            error_flg = True
            print('アクセス解析クリックエラー')

    # モバイル日別アクセス数レポートクリック
    if error_flg is False:
        try:
            report_btn = driver.find_element_by_xpath(
                '/html/body/div[4]/div[9]/div[2]/div[2]/div[1]/div[2]/table/tbody/tr[3]/td[4]/a')
            report_btn.click()
            sleep(1)
            print('日別アクセス数レポート btn click OK!')
        except Exception:
            error_flg = True
            print('日別アクセス数レポートクリックエラー')

    try:
        df_lists = []
        i = 2
        while i >= 0:
            # 月選択
            month_select_elem = driver.find_element_by_id('report-month-first')
            month_select_object = Select(month_select_elem)
            month_select_object.select_by_index(i)
            sleep(1)

            # ここにデータ取得コードを。
            df_list = pd.read_html(driver.page_source)
            df_lists.append(df_list[0])

            i -= 1

    except Exception:
        error_flg = True
        print('データ収集エラー')

    df_list_fix = []
    for df in df_lists:
        df.drop(df.tail(1).index, inplace=True)
        df.set_index("日付", inplace=True)
        df.index = df.index.str.rstrip('(月火水木金土日)')
        df.index = pd.to_datetime(df.index)
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

    df_fix = pd.concat([df_list_fix[i] for i in range(0, len(df_list_fix))])
    print('create df_list')

    now = dt.datetime.now().strftime('%Y%m%d')
    oldpath = 'data_garage_tb_sp_{}.csv'.format(now)
    response = HttpResponse(content_type='text/csv; charset=UTF-8-sig')
    response['Content-Disposition'] = 'attachment; filename={}'.format(oldpath)
    df_fix.to_csv(path_or_buf=response, float_format='%.2f', decimal=",")

    sleep(1)
    driver.quit()

    return response
    # return render(request, 'scr/garage_hp.html')
