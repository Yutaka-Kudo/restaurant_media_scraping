from numpy import true_divide
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# import chromedriver_binary
from time import sleep, time
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta
# import itertools
import os
from django.http import HttpResponse, HttpResponseRedirect

# from django.shortcuts import render
from django.shortcuts import render, redirect
# from django.views.generic import TemplateView
# from django.urls import reverse


from scraping.site_package.driver_settings import options

from scraping import models
from scraping import pwd


def gn_sp(request):
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
    # driver.implicitly_wait(5)
    # wait = WebDriverWait(driver, 10)

    print('Browser is ready!')
    driver.set_page_load_timeout(3.7)

    for store_name in store_list:
        # 店舗選択
        if store_name == "fes":
            user_name = pwd.fgi
            pw = pwd.fgp
            dbmodel = models.Fes_gn_scrape
        elif store_name == "garage":
            user_name = pwd.ggi
            pw = pwd.ggp
            dbmodel = models.Grg_gn_scrape
        elif store_name == "tourou":
            user_name = pwd.tgi
            pw = pwd.tgp
            dbmodel = models.Toro_gn_scrape
        elif store_name == "wanaichi":
            user_name = pwd.wgi
            pw = pwd.wgp
            dbmodel = models.Wana_gn_scrape
        elif store_name == "wananakame":
            user_name = pwd.wngi
            pw = pwd.wngp
            dbmodel = models.Wananakame_gn_scrape
        else:
            user_name, pw = None, None
            driver.quit()
            raise Exception('店舗選択エラー1')

        try:
            driver.get("https://pro.gnavi.co.jp/")
        except Exception:
            driver.execute_script("window.stop();")

        # 2回転目用
        try:
            sleep(2)
            driver.find_element_by_link_text("ログアウト").click()
        except Exception:
            driver.execute_script("window.stop();")

        # フォーム取得
        try:
            sleep(2)
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
            id_input.send_keys(user_name)
            pw_input.send_keys(pw)
            print('input OK!')
            # sleep(1)
            pw_input.submit()
        except Exception:
            driver.execute_script("window.stop();")
            #

            #

        # driver.set_page_load_timeout(10)
        try:
            sleep(2)
            elem = driver.find_element_by_xpath('/html/body/center/div/div[3]/div[1]/div[1]/input')
            print('in btn catch!')
        except Exception:
            print('in btn catch NG')
            driver.quit()

        #
        try:
            # elem = WebDriverWait(driver, timeout=4).until(EC.presence_of_element_located((By.XPATH, '/html/body/center/div/div[3]/div[1]/div[1]/input')))
            # elem.click()
            elem.click()
        except Exception:
            print('in btn click!')
            driver.execute_script("window.stop();")

            #

        # 未確認情報存在時
        try:
            sleep(2)
            elem = driver.find_element_by_id('js-unconfirmedRsvModalClose')
            elem.click()
            print('未確認情報OK!')
        except Exception:
            pass

        # GONアクセス集計　クリック
        #
        try:
            # elem = wait.until(EC.presence_of_element_located(
            #     (By.XPATH, '//input[@value="アクセス状況の詳細を確認"]')))
            sleep(2)
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

        # # ↑別のやり方
        # elem = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH,'//input[@value="アクセス状況の詳細を確認"]')))

        # SP　クリック
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
        sleep(1)
        for date in span_list:
            try:
                # 月選択
                sleep(2)
                month_select_elem = driver.find_element_by_id('ym')
                month_select_object = Select(month_select_elem)
                month_select_object.select_by_value(date)
                sleep(2) # これ絶対ひつよう
                df_list = pd.read_html(driver.page_source)
                df = df_list[0]

            except Exception:
                driver.quit()
                raise Exception('データ収集エラー')

            try:

                df = df.T.reset_index(level=0, drop=True).T
                df.drop(df.tail(3).index, inplace=True)
                df.set_index(df.columns[0], inplace=True)
                df.index = df.index.str.rstrip('(月火水木金土日)')
                df.index = pd.to_datetime(df.index, format='%Y/%m/%d')
                df.drop('天気', axis=1, inplace=True)
                
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
                raise Exception('df fix NG')

            print('create df_list')

            month = df.index.astype(str)
            month_fix = month[0][:7]  # 最初だけ month_key用

            for s in df.itertuples():
                dbmodel.objects.update_or_create(
                    date=s[0],
                    defaults={
                        "week": s[1],
                        "total_pv_sp": s[2],
                        "top_pv_sp": s[3],
                        "menu_pv_sp": s[4],
                        "seat_pv_sp": s[5],
                        "photo_pv_sp": s[6],
                        "commitment_pv_sp": s[7],
                        "map_pv_sp": s[8],
                        "coupon_pv_sp": s[9],
                        "reserve_pv_sp": s[10],
                        "month_key": month_fix,
                    }
                )
        # PC
        try:
            sleep(2)
            elem = driver.find_element_by_xpath("//a[text()='PC']")
            print('PC btn catch!')
        except Exception:
            print('PC btn catch NG')
            driver.quit()
        try:
            elem.click()
            print('PC btn click!')
        except Exception:
            print('PC btn click!')
            driver.execute_script("window.stop();")
        sleep(1)
        for date in span_list:
            try:
                # 月選択
                sleep(2)
                month_select_elem = driver.find_element_by_id('ym')
                month_select_object = Select(month_select_elem)
                month_select_object.select_by_value(date)
                sleep(2) # これ絶対ひつよう
                df_list = pd.read_html(driver.page_source)
                df = df_list[0]

            except Exception:
                driver.quit()
                raise Exception('データ収集エラー')

            try:
                df = df.T.reset_index(level=0, drop=True).T
                df.drop(df.tail(3).index, inplace=True)
                df.drop('その他',axis=1,inplace=True)
                df.drop('天気', axis=1, inplace=True)
                df.set_index(df.columns[0], inplace=True)
                df.index = df.index.str.rstrip('(月火水木金土日)')
                df.index = pd.to_datetime(df.index, format='%Y/%m/%d')
            except Exception:
                driver.quit()
                raise Exception('df fix NG')

            print('create df_list')

            for s in df.itertuples():
                dbmodel.objects.update_or_create(
                    date=s[0],
                    defaults={
                        "total_pv_pc": s[1],
                        "top_pv_pc": s[2],
                        "menu_pv_pc": s[3],
                        "seat_pv_pc": s[4],
                        "photo_pv_pc": s[5],
                        "commitment_pv_pc": s[6],
                        "map_pv_pc": s[7],
                        "coupon_pv_pc": s[8],
                        "reserve_pv_pc": s[9],
                    }
                )

        # app
        try:
            sleep(2)
            elem = driver.find_element_by_xpath("//a[text()='スマートフォンアプリ']")
            print('PC btn catch!')
        except Exception:
            print('PC btn catch NG')
            driver.quit()
        try:
            elem.click()
            print('PC btn click!')
        except Exception:
            print('PC btn click!')
            driver.execute_script("window.stop();")
        sleep(1)
        for date in span_list:
            try:
                # 月選択
                sleep(2)
                month_select_elem = driver.find_element_by_id('ym')
                month_select_object = Select(month_select_elem)
                month_select_object.select_by_value(date)
                sleep(2) # これ絶対ひつよう
                df_list = pd.read_html(driver.page_source)
                df = df_list[0]

            except Exception:
                driver.quit()
                raise Exception('データ収集エラー')

            try:
                df = df.T.reset_index(level=0, drop=True).T
                df.drop(df.tail(3).index, inplace=True)
                df.drop('天気', axis=1, inplace=True)
                df.set_index(df.columns[0], inplace=True)
                df.index = df.index.str.rstrip('(月火水木金土日)')
                df.index = pd.to_datetime(df.index, format='%Y/%m/%d')
            except Exception:
                driver.quit()
                raise Exception('df fix NG')

            print('create df_list')

            for s in df.itertuples():
                dbmodel.objects.update_or_create(
                    date=s[0],
                    defaults={
                        "total_pv_app": s[1],
                        "top_pv_app": s[2],
                        "menu_pv_app": s[3],
                        "seat_pv_app": s[4],
                        "photo_pv_app": s[5],
                        "commitment_pv_app": s[6],
                        "map_pv_app": s[7],
                        "coupon_pv_app": s[8],
                        "reserve_pv_app": s[9],
                    }
                )

        # 予約数取得
        for date in span_list:
            try:
                sleep(2)
                reserve_count_btn = driver.find_element_by_link_text('予約受付数')
                reserve_count_btn.click()
                month_select_elem = driver.find_element_by_id('ym')
                month_select_object = Select(month_select_elem)
                month_select_object.select_by_value(date)
                sleep(2)
                df = pd.read_html(driver.page_source)[0]
            except Exception:
                driver.quit()
                raise Exception('データ収集エラー2')

            try:
                df = df.T.reset_index(level=0, drop=True).T
                df = df.drop([df.index[-1],df.index[-2],df.index[-3]])
                df.set_index(df.columns[0], inplace=True)
                df.index = df.index.str.rstrip('(月火水木金土日)')
                df.index = pd.to_datetime(df.index, format='%Y/%m/%d')
            except Exception:
                driver.quit()
                raise Exception('df fix NG2')

            print('create df_list2')

            for s in df.itertuples():
                dbmodel.objects.update_or_create(
                    date=s[0],
                    defaults={
                        "reserve_course_number": s[1],
                        "reserve_course_people": s[2],
                        "reserve_course_price": s[3],
                        "reserve_seatonly_number": s[4],
                        "reserve_seatonly_people": s[5],
                        "reserve_request_number": s[6],
                        "reserve_request_people": s[7],
                        "reserve_total": s[8],
                    }
                )

            # df_fix = pd.concat([df_list_fix[i] for i in range(0, len(df_list_fix))])
            print(date)
    driver.quit()

    return redirect("/dev/")
    # return render(request, "scr/index.html")
