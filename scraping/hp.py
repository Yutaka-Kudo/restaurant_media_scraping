from selenium import webdriver
from selenium.webdriver.support.select import Select
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
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
# import os

from scraping import models
from scraping import pwd

from scraping.site_package.driver_settings import options


def hp_sp(request):
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

    driver.get("https://www.cms.hotpepper.jp/CLN/login/")

    print('get url!')
    # sleep(1)

    # フォーム取得
    id_input = driver.find_element_by_xpath(
        "/html/body/div[2]/div/form/div/div[2]/table/tbody/tr[1]/td/input")
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
        id_input.send_keys(pwd.hpi)
        pw_input.send_keys(pwd.hpp)
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
        sleep(1)
        print(f'{store_name} select OK!')

        # 未確認情報
        try:
            driver.find_element_by_link_text('閉じる').click()
            print('未確認情報OK！')
            # sleep(1)
        except Exception:
            pass
        try:
            driver.find_element_by_class_name('modalCloseBtn').click()
            print('未確認情報OK！2')
            # sleep(1)
        except Exception:
            pass

        # レポートボタンクリック
        try:
            report_btn = driver.find_element_by_link_text('アクセス・レポート')
            report_btn.click()
            sleep(1)
            print('report btn click OK!')
        except Exception:
            driver.quit()
            raise Exception('レポートボタンクリックエラー')

        handle_array = driver.window_handles
        print(handle_array[0])
        print(handle_array[1])
        # 操作ウィンドウを変更する
        driver.switch_to.window(handle_array[-1])
        sleep(1)
        print('handle OK!')

        try:
            for date in span_list:
                # 月選択
                month_select_elem = driver.find_element_by_name('numberCd')
                month_select_object = Select(month_select_elem)
                month_select_object.select_by_value(date)
                sleep(1)
                # SPクリック
                driver.find_element_by_xpath(
                    '/html/body/div[2]/div/div/form/div[3]/table/tbody/tr/td/label[2]/input').click()

                # ここにデータ取得コードを。
                df_list = pd.read_html(driver.page_source)
                df_list[4]

                month = df_list[4].iloc[10, 0].astype(str)[:6]
                month_fix = month[:4]+"-"+month[4:6]
                # データ整形
                df_list[4].set_index('日付', inplace=True)
                df_list[4].index = pd.to_datetime(df_list[4].index, format='%Y%m%d')
                df_list[4].fillna(0, inplace=True)

                for s in df_list[4].itertuples():
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
                            "reserve_hp": s[8],
                            "reserve_homepage": s[9],
                            "day_over_day_changes": s[10],
                            "month_key": month_fix,
                        }
                    )

                print(f'{date} insert db!')
        except Exception:
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

        # sleep(1)
    driver.quit()

    return redirect("/dev/")
    # return render(request, 'scr/garage_hp.html')
