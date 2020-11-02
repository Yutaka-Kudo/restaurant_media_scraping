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
import os
from django.http import HttpResponse, HttpResponseRedirect

# from django.shortcuts import render
from django.shortcuts import render, redirect
# from django.views.generic import TemplateView
# from django.urls import reverse

from . import pwd

from .driver_settings import options

from .models import Wana_gn_sp_scrape


def wana_gn_sp(request):

    driver = webdriver.Chrome(chrome_options=options)
    # driver.set_window_size(1250, 1036)
    # driver.implicitly_wait(5)
    # wait = WebDriverWait(driver, 10)

    print('Browser is ready!')
    driver.set_page_load_timeout(3.7)

    try:
        url = "https://pro.gnavi.co.jp/"
        driver.get(url)
    except Exception:
        driver.execute_script("window.stop();")

    user_name = pwd.wgi
    pw = pwd.wgp

    # フォーム取得
    try:
        id_input = driver.find_element_by_id("loginID")
        pw_input = driver.find_element_by_id('input_password')
        print('open url!')
    except Exception:
        print('non open')
        driver.quit()

    # 中身をクリア
    # id_input.clear()
    # pw_input.clear()

    try:
        # 入力
        # driver.find_element_by_xpath(
        #     "/html/body/main/div[2]/div/div/div[2]/dl/dd/form/div[3]/div[1]/label").click()
        id_input.send_keys(user_name)
        pw_input.send_keys(pw)
        print('input OK!')
        # sleep(1)
        pw_input.submit()
    except Exception:
        driver.execute_script("window.stop();")
        # error_flg = True

        # error_flg = True

    # driver.set_page_load_timeout(10)
    try:
        elem = driver.find_element_by_xpath('/html/body/center/div/div[3]/div[1]/div[1]/input')
        print('in btn catch!')
    except Exception:
        print('in btn catch NG')
        driver.quit()

    # if error_flg is False:
    try:
        # elem = WebDriverWait(driver, timeout=4).until(EC.presence_of_element_located((By.XPATH, '/html/body/center/div/div[3]/div[1]/div[1]/input')))
        # elem.click()
        elem.click()
    except Exception:
        print('in btn click!')
        driver.execute_script("window.stop();")

        # error_flg = True

    # 未確認情報存在時
    try:
        elem = driver.find_element_by_id('js-unconfirmedRsvModalClose')
        elem.click()
        print('未確認情報OK!')
        sleep(1)
    except Exception:
        pass

    # GONアクセス集計　クリック
    # if error_flg is False:
    try:
        # elem = wait.until(EC.presence_of_element_located(
        #     (By.XPATH, '//input[@value="アクセス状況の詳細を確認"]')))
        elem = driver.find_element_by_xpath('//input[@value="アクセス状況の詳細を確認"]')
        print('GON catch!')
    except Exception:
        print('GON catch NG')
        driver.quit()

    try:
        elem.click()
        print('GON click!')
    except Exception:
        print('GON click!')
        driver.execute_script("window.stop();")
        # error_flg = True

    # # ↑別のやり方
    # elem = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH,'//input[@value="アクセス状況の詳細を確認"]')))

    # In[16]:

    # SP　クリック
    # if error_flg is False:
    try:
        sleep(2)
        elem = driver.find_element_by_xpath("//a[text()='スマートフォン']")
        print('SP btn catch!')
    except Exception:
        print('SP btn catch NG')
        driver.quit()

    try:
        elem.click()
        print('SP btn click!')
    except Exception:
        print('SP btn click!')
        driver.execute_script("window.stop();")
        # driver.execute_script("window.stop();")
        # error_flg = True

    # In[17]:
    sleep(1)
    # 本番用
    # if error_flg is False:
    try:
        i = request.GET.get('w')
        print(i)
        # 月選択
        month_select_elem = driver.find_element_by_id('ym')
        month_select_object = Select(month_select_elem)
        month_select_object.select_by_index(i)
        sleep(2)

        # ここにデータ取得コードを。
        df_list = pd.read_html(driver.page_source)
        df = df_list[0]

    except Exception:
        # error_flg = True
        print('データ収集エラー')
        driver.quit()

    # In[18]:

    # In[19]:

    try:

        df.columns = ['日にち', "天気", "合計", '店舗トップ', 'メニュー',
                      '席・個室・貸切', '写真', 'こだわり', '地図', 'クーポン', '予約']
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

    except Exception:
        print('fix NG')
        driver.quit()

    print('create df_list')

    month = df.index.astype(str)
    month_fix = month[0][:7]

    # for s in df.itertuples():
    #     Fes_gn_sp_scrape.objects.create(
    #         date=s[0],
    #         week=s[1],
    #         total=s[2],
    #         top=s[3],
    #         menu=s[4],
    #         seat=s[5],
    #         photo=s[6],
    #         commitment=s[7],
    #         map=s[8],
    #         coupon=s[9],
    #         reserve=s[10],
    #         month_key=month_fix,
    #     )
    for s in df.itertuples():
        Wana_gn_sp_scrape.objects.update_or_create(
            date=s[0],
            defaults={
                "week": s[1],
                "total": s[2],
                "top": s[3],
                "menu": s[4],
                "seat": s[5],
                "photo": s[6],
                "commitment": s[7],
                "map": s[8],
                "coupon": s[9],
                "reserve": s[10],
                "month_key": month_fix,
            }
        )

    # In[20]:

    # df_fix = pd.concat([df_list_fix[i] for i in range(0, len(df_list_fix))])

    driver.quit()

    return redirect("/dev/")
    # return render(request, "scr/index.html")
