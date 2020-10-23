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
import os

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
# from django.views.generic import TemplateView
# from django.urls import reverse

# from .models import Scraping


from .driver_settings import options

# import random
from .models import Wana_tb_sp_scrape


def wana_tb_sp(request):
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
        driver.quit()

    if error_flg is False:
        try:
            pw_input.submit()
            sleep(1)
            print('login OK!')
        except Exception:
            error_flg = True
            print('ログインエラー')
            driver.quit()

    # 店舗選択
    if error_flg is False:
        try:
            elem = driver.find_element(
                By.XPATH, ('/html/body/div[4]/div[2]/ul/li[11]/div[2]/form/input[4]'))
            elem.click()
            sleep(1)
            print('store select OK!')
        except Exception:
            error_flg = True
            print('店舗選択エラー')
            driver.quit()

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
            driver.quit()

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
            driver.quit()

    try:
        i = request.GET.get('w')
        # 月選択
        month_select_elem = driver.find_element_by_id('report-month-first')
        month_select_object = Select(month_select_elem)
        month_select_object.select_by_index(i)
        sleep(1)

        # ここにデータ取得コードを。
        df_list = pd.read_html(driver.page_source)
        df = df_list[0]
    except Exception:
        error_flg = True
        print('データ収集エラー')
        driver.quit()

    try:
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
    except Exception:
        print('fix NG')
        driver.quit()

    print('create df_list')

    # df_fix = pd.concat([df_list_fix[i] for i in range(0, len(df_list_fix))])
    # print('create df_list')
    month = df.index.astype(str)
    month_fix = month[0][:7]

    for s in df.itertuples():
        Wana_tb_sp_scrape.objects.update_or_create(
            date=s[0],
            defaults={
                "week": s[1],
                "top": s[2],
                "photo": s[3],
                "photo_info": s[4],
                "rating": s[5],
                "menu": s[6],
                "map": s[7],
                "coupon": s[8],
                "p_coupon": s[9],
                "seat": s[10],
                "other": s[11],
                "total": s[12],
                "month_key": month_fix,
            }
        )

    sleep(1)
    driver.quit()

    return redirect('/dev/')
    # return render(request, 'scr/garage_hp.html')
