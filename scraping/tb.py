from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# import chromedriver_binary
from time import sleep
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta

# import itertools
import os

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
# from django.views.generic import TemplateView
# from django.urls import reverse

# from .models import Scraping

from scraping import models
from scraping import pwd

from scraping.site_package.driver_settings import options

# import random


def tb_sp(request):
    # 選択店取得
    store_list = [request.GET.get("fes"), request.GET.get("garage"), request.GET.get("tourou"), request.GET.get("wanaichi"), request.GET.get("wananakame")]
    store_list = list(filter(None, store_list))  # Noneを除外
    print(store_list)

    # 期間リスト作成ーーーーーーー
    start_year: str = request.GET.get("start_year")
    start_month: str = request.GET.get("start_month")
    start_ym = start_year + start_month
    end_year: str = request.GET.get("end_year")
    end_month: str = request.GET.get("end_month")
    end_ym = end_year + end_month

    span_list = []
    start_ym, end_ym = [datetime.strptime(d, "%Y%m").date() for d in [start_ym, end_ym]]
    if start_ym < end_ym:
        while start_ym <= end_ym:
            span_list.append(start_ym.strftime('%Y%m'))
            start_ym += relativedelta(months=1)
    else:
        while start_ym >= end_ym:
            span_list.append(end_ym.strftime('%Y%m'))
            end_ym += relativedelta(months=1)
    print(span_list)

    driver = webdriver.Chrome(chrome_options=options)
    # driver.set_window_size(1250, 1036)
    driver.implicitly_wait(5)

    print('Browser is ready!')

    driver.get("https://ssl.tabelog.com/owner_account/login/")

    print('get url!')
    # sleep(1)

    user_name = pwd.tbi
    pw = pwd.tbp

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
        driver.quit()
        raise Exception('インプットエラー')

    try:
        pw_input.submit()
        sleep(1)
        print('login OK!')
    except Exception:
        driver.quit()
        raise Exception('ログインエラー')

    def get_data(store_name):
        # 店舗選択
        if store_name == "fes":
            elem = driver.find_element(
                By.XPATH, ("/html/body/div[4]/div[2]/ul/li[8]/div[2]/form/input[4]"))
            dbmodel = models.Fes_tb_scrape
        elif store_name == "garage":
            elem = driver.find_element(
                By.XPATH, ("/html/body/div[4]/div[2]/ul/li[4]/div[2]/form/input[4]"))
            dbmodel = models.Grg_tb_scrape
        elif store_name == "tourou":
            elem = driver.find_element(
                By.XPATH, ("/html/body/div[4]/div[2]/ul/li[10]/div[2]/form/input[4]"))
            dbmodel = models.Toro_tb_scrape
        elif store_name == "wanaichi":
            elem = driver.find_element(
                By.XPATH, ('/html/body/div[4]/div[2]/ul/li[11]/div[2]/form/input[4]'))
            dbmodel = models.Wana_tb_scrape
        elif store_name == "wananakame":
            elem = driver.find_element(
                By.XPATH, ("/html/body/div[4]/div[2]/ul/li[13]/div[2]/form/input[4]"))
            dbmodel = models.Wananakame_tb_scrape
        else:
            elem = None
            driver.quit()
            raise Exception('店舗選択エラー1')

        elem.click()
        sleep(1)
        print('store select OK!')

        # 未確認情報
        try:
            driver.find_elements_by_class_name('owner-alert-modal__close-target')[1].click()
            print('未確認情報OK！')
            # sleep(1)
        except Exception:
            pass

        # アクセス解析クリック

        try:
            report_btn = driver.find_element_by_link_text('アクセス解析')
            report_btn.click()
            sleep(1)
            print('アクセス解析 btn click OK!')
        except Exception:
            driver.quit()
            raise Exception('アクセス解析クリックエラー')

        # モバイル日別アクセス数レポートクリック

        try:
            report_btn = driver.find_element_by_xpath(
                '/html/body/div[4]/div[9]/div[2]/div[2]/div[1]/div[2]/table/tbody/tr[3]/td[4]/a')
            report_btn.click()
            sleep(1)
            print('日別アクセス数レポート btn click OK!')
        except Exception:
            driver.quit()
            raise Exception('日別アクセス数レポートクリックエラー')

        for date in span_list:
            try:
                # 月選択
                month_select_elem = driver.find_element_by_id('report-month-first')
                month_select_object = Select(month_select_elem)
                month_select_object.select_by_value(date)
                sleep(1)

                # ここにデータ取得コードを。
                df_list = pd.read_html(driver.page_source)
                df = df_list[0]
            except Exception:
                driver.quit()
                raise Exception('データ収集エラー')

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
                driver.quit()
                raise Exception('fix NG')

            print('create df_list')

            # df_fix = pd.concat([df_list_fix[i] for i in range(0, len(df_list_fix))])
            # print('create df_list')
            month = df.index.astype(str)
            month_fix = month[0][:7]

            for s in df.itertuples():
                dbmodel.objects.update_or_create(
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

    # 本体ーーーーーーー
    for store_name in store_list:
        get_data(store_name)
        driver.get("https://ssl.tabelog.com/owner_account/rstgrp/")

    sleep(1)
    driver.quit()

    return redirect('/dev/')
    # return render(request, 'scr/garage_hp.html')
