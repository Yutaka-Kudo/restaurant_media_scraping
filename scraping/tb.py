from scraping.views import index
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


def capture(driver):
    n = datetime.now()
    FILENAME = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), f"static/images/screen{n.date()}{n.hour}{n.minute}.png")
    w = driver.execute_script('return document.body.scrollWidth;')
    h = driver.execute_script('return document.body.scrollHeight;')
    driver.set_window_size(w, h)
    driver.save_screenshot(FILENAME)


def tb_sp(request, all: bool = False):
    # 選択店取得
    store_list = [request.GET.get("fes"), request.GET.get("garage"), request.GET.get("tourou"), request.GET.get("wanaichi"), request.GET.get("wananakame")]
    store_list = list(filter(None, store_list))  # Noneを除外
    if all is True:
        store_list = ["fes","garage","tourou","wanaichi","wananakame"]
    print(store_list)

    # 期間リスト作成ーーーーーーー
    if all is False:
        start_year: str = request.GET.get("start_year")
        start_month: str = request.GET.get("start_month")
        start_ym = start_year + start_month
        end_year: str = request.GET.get("end_year")
        end_month: str = request.GET.get("end_month")
        end_ym = end_year + end_month

        span_list = []
        start_ym, end_ym = [datetime.strptime(d, "%Y%m").date() for d in [start_ym, end_ym]]

        if start_ym > datetime.now().date() or end_ym > datetime.now().date():
            raise Exception('未来の日にちですよ。')

        if start_ym < end_ym:
            while start_ym <= end_ym:
                span_list.append(start_ym.strftime('%Y%m'))
                start_ym += relativedelta(months=1)
        else:
            while start_ym >= end_ym:
                span_list.append(end_ym.strftime('%Y%m'))
                end_ym += relativedelta(months=1)
    if all is True:
        span_list = [(datetime.now().date()-relativedelta(days=1)).strftime('%Y%m')]
        start_year = span_list[0][:4]
        start_month = span_list[0][4:]
        end_year = start_year
        end_month = start_month
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
        capture(driver)
        driver.quit()
        raise Exception('インプットエラー')

    try:
        pw_input.submit()
        sleep(1)
        print('login OK!')
    except Exception:
        capture(driver)
        driver.quit()
        raise Exception('ログインエラー')

    def get_data(store_name):
        # 店舗選択
        if store_name == "fes":
            elem = driver.find_element_by_xpath("/html/body/div[4]/div[2]/ul/li[8]/div[2]/form/input[4]")
            # elem = driver.find_element(
            #     By.XPATH, ("/html/body/div[4]/div[2]/ul/li[8]/div[2]/form/input[4]"))
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
            capture(driver)
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
            capture(driver)
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
                    capture(driver)
                    driver.quit()
                    raise Exception('fix NG')

                print('create df_list')

                # df_fix = pd.concat([df_list_fix[i] for i in range(0, len(df_list_fix))])
                # print('create df_list')
                month = df.index.astype(str)
                month_key = month[0][:7]

                for s in df.itertuples():
                    dbmodel.objects.update_or_create(
                        date=s[0],
                        defaults={
                            "week": s[1],
                            "top_pv_sp": s[2],
                            "photo_pv_sp": s[3],
                            "photo_info_pv_sp": s[4],
                            "rating_pv_sp": s[5],
                            "menu_pv_sp": s[6],
                            "map_pv_sp": s[7],
                            "coupon_pv_sp": s[8],
                            "p_coupon_pv_sp": s[9],
                            "seat_pv_sp": s[10],
                            "other_pv_sp": s[11],
                            "total_pv_sp": s[12],
                            "month_key": month_key,
                        }
                    )

                # PCーーーーーーーー
                try:
                    report_btn = driver.find_element_by_link_text('PC版')
                    report_btn.click()
                    sleep(1)
                    print('日別アクセス数レポート btn click OK!')
                except Exception:
                    capture(driver)
                    driver.quit()
                    raise Exception('PC版 クリックエラー')

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
                        capture(driver)
                        driver.quit()
                        raise Exception('データ収集エラー')

                    try:
                        df.drop(df.tail(1).index, inplace=True)
                        for i in df.columns:  # 名前怪しいので。地図印刷 *3 になってる。
                            if "地図印刷" in i:
                                df.drop(i, axis=1, inplace=True)
                        df.set_index("日付", inplace=True)
                        df.index = df.index.str.rstrip('(月火水木金土日)')
                        df.index = pd.to_datetime(df.index)
                    except Exception:
                        capture(driver)
                        driver.quit()
                        raise Exception('fix NG')
                    print('create df_list')

                    for s in df.itertuples():
                        dbmodel.objects.update_or_create(
                            date=s[0],
                            defaults={
                                "top_pv_pc": s[1],
                                "photo_food_pv_pc": s[2],
                                "photo_drink_pv_pc": s[3],
                                "photo_interior_pv_pc": s[4],
                                "photo_exterior_pv_pc": s[5],
                                "rating_pv_pc": s[6],
                                "menu_pv_pc": s[7],
                                "map_coupon_pv_pc": s[8],
                                "p_coupon_pv_pc": s[9],
                                "seat_pv_pc": s[10],
                                "other_pv_pc": s[11],
                                "total_pv_pc": s[12],
                            }
                        )
            except Exception:
                try:
                    driver.find_element_by_link_text('直近1ヶ月').click()

                    # ここにデータ取得コードを。
                    df_list = pd.read_html(driver.page_source)
                    df = df_list[0]
                except Exception:
                    capture(driver)
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
                    capture(driver)
                    driver.quit()
                    raise Exception('fix NG')

                print('create df_list')

                for s in df.itertuples():
                    dbmodel.objects.update_or_create(
                        date=s[0],
                        defaults={
                            "week": s[1],
                            "top_pv_sp": s[2],
                            "photo_pv_sp": s[3],
                            "photo_info_pv_sp": s[4],
                            "rating_pv_sp": s[5],
                            "menu_pv_sp": s[6],
                            "map_pv_sp": s[7],
                            "coupon_pv_sp": s[8],
                            "p_coupon_pv_sp": s[9],
                            "seat_pv_sp": s[10],
                            "other_pv_sp": s[11],
                            "total_pv_sp": s[12],
                            "month_key": str(s[0])[:7],
                        }
                    )

                # PCーーーーーーーー
                try:
                    report_btn = driver.find_element_by_link_text('PC版')
                    report_btn.click()
                    sleep(1)
                    print('日別アクセス数レポート btn click OK!')
                except Exception:
                    capture(driver)
                    driver.quit()
                    raise Exception('PC版 クリックエラー')

                for date in span_list:
                    try:
                        # ここにデータ取得コードを。
                        df_list = pd.read_html(driver.page_source)
                        df = df_list[0]
                    except Exception:
                        capture(driver)
                        driver.quit()
                        raise Exception('データ収集エラー')

                    try:
                        df.drop(df.tail(1).index, inplace=True)
                        for i in df.columns:  # 名前怪しいので。地図印刷 *3 になってる。
                            if "地図印刷" in i:
                                df.drop(i, axis=1, inplace=True)
                        df.set_index("日付", inplace=True)
                        df.index = df.index.str.rstrip('(月火水木金土日)')
                        df.index = pd.to_datetime(df.index)
                    except Exception:
                        capture(driver)
                        driver.quit()
                        raise Exception('fix NG')
                    print('create df_list')

                    for s in df.itertuples():
                        last_day = datetime.strptime(str(s[0])[:10], '%Y-%m-%d').date()
                        dbmodel.objects.update_or_create(
                            date=s[0],
                            defaults={
                                "top_pv_pc": s[1],
                                "photo_food_pv_pc": s[2],
                                "photo_drink_pv_pc": s[3],
                                "photo_interior_pv_pc": s[4],
                                "photo_exterior_pv_pc": s[5],
                                "rating_pv_pc": s[6],
                                "menu_pv_pc": s[7],
                                "map_coupon_pv_pc": s[8],
                                "p_coupon_pv_pc": s[9],
                                "seat_pv_pc": s[10],
                                "other_pv_pc": s[11],
                                "total_pv_pc": s[12],
                            }
                        )

        # ネット予約管理画面
        driver.find_element_by_class_name("ogly-b-calendar").click()
        # 予約台帳
        driver.find_element_by_link_text("予約台帳").click()
        sleep(2)
        # カレンダー
        driver.find_element_by_class_name("ogly-b-calendar").click()
        # iframeにスイッチ
        driver.switch_to_frame(driver.find_element_by_id("js-panel-frame"))

        for date in reversed(span_list):  # span_listを最近の日付から取り出す。
            def trans____year__month(date: str) -> str:
                return date[:4]+"年" + " "+str(int(date[4:])) + "月"

            while trans____year__month(date) != driver.find_element_by_xpath('/html/body/div/table/caption').text:  # ex. '2021年 2月'
                driver.find_element_by_class_name('gly-b-prev').click()
                sleep(1)

            df = pd.read_html(driver.page_source)[0]
            index_list = list(df.index)
            for index, row in df.iterrows():
                for d in row:
                    if index == index_list[0]:  # 前月、次月の日以外
                        if type(d) == int:  # なぜかたまにintが混じる
                            d = str(d)
                        if int(d[:2]) < 10:  # 前月、次月の日以外
                            if "：" in d:
                                d_splited = d.split(' ')
                                for s in d_splited:
                                    if "：" in s:
                                        s_splited = s.split('：')
                                        result = s_splited[1][:-1]
                                        day = datetime.strptime(date+str(int(d[:2])).zfill(2), '%Y%m%d').date()
                                        if day <= last_day:
                                            dbmodel.objects.update_or_create(
                                                date=day,
                                                defaults={
                                                    "net_reserve": result,
                                                }
                                            )
                            else:
                                day = datetime.strptime(date+str(int(d[:2])).zfill(2), '%Y%m%d').date()
                                if day <= last_day:
                                    dbmodel.objects.update_or_create(
                                        date=day,
                                        defaults={
                                            "net_reserve": 0,
                                        }
                                    )

                    elif index == index_list[-1]:  # 前月、次月の日以外
                        if type(d) == int:  # なぜかたまにintが混じる
                            d = str(d)
                        if int(d[:2]) > 10:  # 前月、次月の日以外
                            if "：" in d:
                                d_splited = d.split(' ')
                                for s in d_splited:
                                    if "：" in s:
                                        s_splited = s.split('：')
                                        result = s_splited[1][:-1]
                                        day = datetime.strptime(date+str(int(d[:2])).zfill(2), '%Y%m%d').date()
                                        if day <= last_day:
                                            dbmodel.objects.update_or_create(
                                                date=day,
                                                defaults={
                                                    "net_reserve": result,
                                                }
                                            )
                            else:
                                day = datetime.strptime(date+str(int(d[:2])).zfill(2), '%Y%m%d').date()
                                if day <= last_day:
                                    dbmodel.objects.update_or_create(
                                        date=day,
                                        defaults={
                                            "net_reserve": 0,
                                        }
                                    )
                    else:
                        if type(d) == int:  # なぜかたまにintが混じる
                            d = str(d)
                        if "：" in d:
                            d_splited = d.split(' ')
                            for s in d_splited:
                                if "：" in s:
                                    s_splited = s.split('：')
                                    result = s_splited[1][:-1]
                                    day = datetime.strptime(date+str(int(d[:2])).zfill(2), '%Y%m%d').date()
                                    if day <= last_day:
                                        dbmodel.objects.update_or_create(
                                            date=day,
                                            defaults={
                                                "net_reserve": result,
                                            }
                                        )
                        else:
                            day = datetime.strptime(date+str(int(d[:2])).zfill(2), '%Y%m%d').date()
                            if day <= last_day:
                                dbmodel.objects.update_or_create(
                                    date=day,
                                    defaults={
                                        "net_reserve": 0,
                                    }
                                )

            # driver.switch_to_default_content()

    # 本体ーーーーーーー
    for store_name in store_list:
        get_data(store_name)
        driver.get("https://ssl.tabelog.com/owner_account/rstgrp/")

    sleep(1)
    driver.quit()

    context = {
        "start_year": start_year,
        "end_year": end_year,
        "start_month": start_month,
        "end_month": end_month,
    }

    return render(request, "scr/dev.html", context)






# # 手動用
# def replace_tax():
#     user_name = pwd.tbi
#     pw = pwd.tbp

#     driver = webdriver.Chrome(chrome_options=options)
#     driver.get("https://ssl.tabelog.com/owner_account/login/")
#     driver.find_element_by_id('login_id').send_keys(user_name)
#     driver.find_element_by_id('password').send_keys(pw).submit()
#     driver.find_element_by_id('password').submit()
#     driver.find_element_by_link_text('店舗ページ編集').click()
#     driver.find_element_by_link_text('メニューの編集').click()
#     driver.find_element_by_xpath('/html/body/div[4]/div[6]/div/div/div[1]/article/section[2]/section[1]/div[1]/div[2]/a').click()


#     folist = driver.find_elements_by_xpath("//input[@type='number']")
#     for fo in folist:
#         if fo.get_attribute('value'):
#             new_price = round(int(fo.get_attribute('value'))*1.1)
#             fo.clear()
#             fo.send_keys(new_price)


#     # メニューページーーーーーーーー
#     menu_descri = driver.find_elements_by_id('menus[][description]')

#     for i in menu_descri:
#         value = i.get_attribute('value')
#         index_num_list = [n for n,v in enumerate(value) if v == "円"]
#         if index_num_list:
#             for position in reversed(index_num_list):
#                 st_posi = position-1
#                 try:
#                     while type(int(value[st_posi])) == int:
#                         st_posi -= 1
#                         if value[st_posi] == ",":
#                             st_posi -= 1
#                 except:
#                     old_price = value[st_posi+1:position].replace(',','')
#                     # print(old_price)
#                     new_price = (int(old_price)*1.1)
#                     # print(new_price)
#                     new_sentence = "(税込{:,.0f}円)".format(new_price)
#                     # print(new_sentence)
#                     value = value[:position+1]+new_sentence+value[position+1:]
#             print(value)
#             i.clear()
#             i.send_keys(value)



    # # ネット予約個別設定
    # for i in range(2,24):
    #     folist = driver.find_elements_by_class_name('js-open-setting-modal')
    #     folist[i].click()
    #     driver.find_element_by_xpath('/html/body/main/div/div/section/div[3]/div/div[2]/div/form/table[1]/tbody/tr[2]/td/div/div/div[2]/label').click()
    #     month_select_elem = driver.find_element_by_id('js-dinner_start') # dinner_start
    #     month_select_object = Select(month_select_elem)
    #     month_select_object.select_by_value("1300")
    #     month_select_elem = driver.find_element_by_id('js-dinner_end') # dinner_end
    #     month_select_object = Select(month_select_elem)
    #     month_select_object.select_by_value("2000")
    #     driver.find_element_by_xpath('/html/body/main/div/div/section/div[3]/div/div[2]/div/form/table[2]/tbody/tr[2]/td/div/div/input').click()
    #     # driver.refresh()
    #     sleep(0.8)


