from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# import chromedriver_binary
from time import sleep
from datetime import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd
from devtools import debug
# import itertools
# import random
# from django.http import HttpResponse, HttpResponseRedirect

# from django.shortcuts import render
# from .models import Scraping
from django.shortcuts import render, redirect
# from django.views.generic import TemplateView
# from django.urls import reverse
import os

from scraping import models
from scraping import pwd

from scraping.site_package.driver_settings import options


def capture(driver):
    n = datetime.now()
    FILENAME = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), f"static/images/screen{n.date()}{n.hour}{n.minute}.png")
    w = driver.execute_script('return document.body.scrollWidth;')
    h = driver.execute_script('return document.body.scrollHeight;')
    driver.set_window_size(w, h)
    driver.save_screenshot(FILENAME)


def hp_sp(request, all: bool = False):
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

    driver.get("https://www.cms.hotpepper.jp/CLN/login/")

    print('get url!')
    # sleep(2)

    # フォーム取得
    id_input = driver.find_element_by_xpath("/html/body/div[2]/div/form/div/div[2]/table/tbody/tr[1]/td/input")
    pw_input = driver.find_element_by_name('password')

    # 中身をクリア
    id_input.clear()
    pw_input.clear()

    sleep(2)

    try:
        # 入力
        id_input.send_keys(pwd.hpi)
        pw_input.send_keys(pwd.hpp)
        print('input OK!')
    except Exception:
        capture(driver)
        driver.quit()
        raise Exception('インプットエラー')

    try:
        pw_input.submit()
        sleep(2)
        print('login OK!')
    except Exception:
        capture(driver)
        driver.quit()
        raise Exception('ログインエラー')

    def get_data(store_name):
        # 店舗選択
        if store_name == "fes":
            elem = driver.find_element_by_link_text('FES by asobi')
            dbmodel = models.Fes_hp_scrape
        elif store_name == "garage":
            elem = driver.find_element_by_link_text('Garage Kitchenあそび　西船橋店')
            dbmodel = models.Grg_hp_scrape
        elif store_name == "tourou":
            elem = driver.find_element_by_link_text('路地ノ裏 灯篭 西船橋店')
            dbmodel = models.Toro_hp_scrape
        elif store_name == "wanaichi":
            elem = driver.find_element_by_link_text('焼ジビエ 罠 一目 船橋店')
            dbmodel = models.Wana_hp_scrape
        elif store_name == "wananakame":
            elem = driver.find_element_by_link_text('焼ジビエ 罠 中目黒店')
            dbmodel = models.Wananakame_hp_scrape
        else:
            elem = None
            driver.quit()
            raise Exception('店舗選択エラー1')

        elem.click()
        sleep(3)
        print(f'{store_name} select OK!')

        # 未確認情報
        try:
            driver.find_element_by_link_text('閉じる').click()
            print('未確認情報OK！')
            sleep(2)
        except Exception:
            pass
        try:
            driver.find_element_by_class_name('modalCloseBtn').click()
            print('未確認情報OK！2')
            sleep(2)
        except Exception:
            pass
        try:
            driver.find_element_by_class_name('jscmodalBtnOrange').click()
            print('未確認情報OK！2')
            sleep(2)
        except Exception:
            pass

        # レポートボタンクリック
        try:
            report_btn = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.LINK_TEXT, 'アクセス・レポート')))
            # report_btn = driver.find_element_by_link_text('アクセス・レポート')
            report_btn.click()
            sleep(2)
            print('report btn click OK!')
        except Exception:
            capture(driver)
            driver.quit()
            raise Exception('レポートボタンクリックエラー')

        handle_array = driver.window_handles
        print(handle_array[0])
        print(handle_array[1])
        # 操作ウィンドウを変更する
        driver.switch_to.window(handle_array[-1])
        sleep(2)
        print('handle OK!')

        try:
            if all is True:
                span_list = range(1,3)
            for date in span_list:
                # 月選択
                month_select_elem = driver.find_element_by_name('numberCd')
                month_select_object = Select(month_select_elem)
                if all is False:
                    month_select_object.select_by_value(date)
                    month: str = date
                else:
                    select_num = date
                    month: str = month_select_object.options[-select_num].get_attribute('value')
                    month_select_object.select_by_index(len(month_select_object.options)-select_num)

                sleep(2)
                # SPクリック
                driver.find_element_by_id('pv_sp').click()

                # ここにデータ取得コードを。
                df = pd.read_html(driver.page_source)[4]
                sleep(2)

                month_key = month[:4]+"-"+month[4:6]
                # データ整形
                df.set_index('日付', inplace=True)
                df.index = pd.to_datetime(df.index, format='%Y%m%d')
                df.drop("前日比", axis=1, inplace=True)
                df.fillna(0, inplace=True)

                for s in df.itertuples():
                    dbmodel.objects.update_or_create(
                        date=s[0],
                        defaults={
                            "week": s[1],
                            "pv_all_sp": s[2],
                            "pv_top_sp": s[3],
                            "pv_coupon_sp": s[4],
                            "cvr_sp": s[5],
                            "tell_sp": s[6],
                            "reserve_sp": s[7],
                            "reserve_hp_sp": s[8],
                            "reserve_homepage_sp": s[9],
                            "month_key": month_key,
                        }
                    )

                print(f'{date} SP insert db!')

                # pcクリック
                driver.find_element_by_id('pv_pc').click()
                sleep(2)

                # ここにデータ取得コードを。
                df = pd.read_html(driver.page_source)[4]
                sleep(1)

                # データ整形
                df.set_index('日付', inplace=True)
                df.index = pd.to_datetime(df.index, format='%Y%m%d')
                df.drop(["曜日", "クーポン印刷PV（PC）", "前日比"], axis=1, inplace=True)

                for s in df.itertuples():
                    dbmodel.objects.update_or_create(
                        date=s[0],
                        defaults={
                            "pv_all_pc": s[1],
                            "pv_top_pc": s[2],
                            "pv_coupon_pc": s[3],
                            "cvr_pc": s[4],
                            "tell_pc": s[5],
                            "reserve_pc": s[6],
                            "reserve_hp_pc": s[7],
                            "reserve_homepage_pc": s[8],
                        }
                    )

                print(f'{date} PC insert db!')

        except Exception:
            capture(driver)
            driver.quit()
            raise Exception('データ収集エラー')

    # 本体ーーーーーーー
    for store_name in store_list:
        get_data(store_name)
        driver.get("https://www.cms.hotpepper.jp/CLN/storeSelect/")

        # In[13]:
        # print('create df_list')

        # basepath, ext = os.path.splitext(os.path.basename(__file__))
        # now = dt.datetime.now().strftime('%Y%m')
        # oldpath = 'data_{}_{}.csv'.format(basepath, now)

        # response = HttpResponse(content_type='text/csv; charset=UTF-8-sig')
        # response['Content-Disposition'] = 'attachment; filename={}'.format(oldpath)
        # df_list[4].to_csv(path_or_buf=response, float_format='%.2f', decimal=",")

        # sleep(2)
    driver.quit()

    context = {
        "start_year": start_year,
        "end_year": end_year,
        "start_month": start_month,
        "end_month": end_month,
    }

    return render(request, "scr/dev.html", context)
