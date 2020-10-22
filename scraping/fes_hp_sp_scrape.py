from selenium import webdriver
from selenium.webdriver.support.select import Select
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# import chromedriver_binary
from time import sleep
import pandas as pd
# import datetime as dt
# import itertools
# import random
# from django.http import HttpResponse, HttpResponseRedirect

# from django.shortcuts import render
# from .models import Scraping
from django.shortcuts import render, redirect
# from django.views.generic import TemplateView
# from django.urls import reverse
# import os

from .models import Fes_hp_sp_scrape

# from rq import Queue
# from worker import conn

from .driver_settings import options


def fes_hp_sp(request):

    error_flg = False

    driver = webdriver.Chrome(chrome_options=options)
    # driver.set_window_size(1250, 1036)
    driver.implicitly_wait(5)

    print('Browser is ready!')

    # In[5]:

    url = "https://www.cms.hotpepper.jp/CLN/login/"
    driver.get(url)

    print('get url!')
    # sleep(1)

    # In[8]:
    user_name = "C329569"
    pw = "fes130!!"

    # In[10]:

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
            elem = driver.find_element_by_link_text('FES by asobi')
            elem.click()
            sleep(1)
            print('store select OK!')
        except Exception:
            error_flg = True
            print('店舗選択エラー')
            driver.quit()
    # In[15]:
    # 未確認情報
    try:
        if driver.find_element_by_link_text('閉じる'):
            driver.find_element_by_link_text('閉じる').click()
            print('未確認情報OK！')
            # sleep(1)
    except Exception:
        pass

        # レポートボタンクリック
    if error_flg is False:
        try:
            report_btn = driver.find_element_by_link_text('アクセス・レポート')
            report_btn.click()
            sleep(1)
            print('report btn click OK!')
        except Exception:
            error_flg = True
            print('レポートボタンクリックエラー')
            driver.quit()

    handle_array = driver.window_handles
    print(handle_array[0])
    print(handle_array[1])
    # 操作ウィンドウを変更する
    driver.switch_to.window(handle_array[-1])
    sleep(1)
    print('handle OK!')

    # In[16]:

    try:
        # 月選択
        month_select_elem = driver.find_element_by_name('numberCd')
        month_select_object = Select(month_select_elem)
        month_select_object.select_by_index(22)  # 23は8月
        sleep(1)
        # SPクリック
        driver.find_element_by_xpath(
            '/html/body/div[2]/div/div/form/div[3]/table/tbody/tr/td/label[2]/input').click()

        # ここにデータ取得コードを。
        df_list = pd.read_html(driver.page_source)
        df_list[4]

    except Exception:
        error_flg = True
        print('データ収集エラー')
        driver.quit()

    month = df_list[4].iloc[8, 0].astype(str)[:6]
    month_fix = month[:4]+"-"+month[4:6]
    # データ整形
    df_list[4].set_index('日付', inplace=True)
    df_list[4].index = pd.to_datetime(df_list[4].index, format='%Y%m%d')
    df_list[4].fillna(0, inplace=True)

    for s in df_list[4].itertuples():
        Fes_hp_sp_scrape.objects.update_or_create(
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

    print('insert db!')
    # In[13]:
    # print('create df_list')

    # basepath, ext = os.path.splitext(os.path.basename(__file__))
    # now = dt.datetime.now().strftime('%Y%m')
    # oldpath = 'data_{}_sp_{}.csv'.format(basepath, now)

    # response = HttpResponse(content_type='text/csv; charset=UTF-8-sig')
    # response['Content-Disposition'] = 'attachment; filename={}'.format(oldpath)
    # df_list[4].to_csv(path_or_buf=response, float_format='%.2f', decimal=",")

    # sleep(1)
    driver.quit()
    return redirect("/fes/")

    
    # return render(request, 'scr/garage_hp.html')
    

