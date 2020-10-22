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
import random
from django.http import HttpResponse, HttpResponseRedirect

# from django.shortcuts import render
# from .models import Scraping
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.urls import reverse
import os



from .driver_settings import options

def toro_hp_sp(request):
    
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
            elem = driver.find_element_by_link_text('路地ノ裏 灯篭 西船橋店')
            elem.click()
            sleep(2)
            print('store select OK!')
        except Exception:
            error_flg = True
            print('店舗選択エラー')
            driver.quit()
    # In[15]:

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
        df_lists = []
        i = 9  # 20
        while i <= 11:
            # 月選択
            month_select_elem = driver.find_element_by_name('numberCd')
            month_select_object = Select(month_select_elem)
            month_select_object.select_by_index(i)
            sleep(1)

            # ここにデータ取得コードを。
            df_list = pd.read_html(driver.page_source)
            df_lists.append(df_list[4])

            i += 1

    except Exception:
        error_flg = True
        print('データ収集エラー')
        driver.quit()

    df_list_fix = []
    for df in df_lists:
        df.set_index('日付', inplace=True)
        df.index = pd.to_datetime(df.index, format='%Y%m%d')
        df_list_fix.append(df)


    # In[13]:
    df_fix = pd.concat([df_list_fix[i] for i in range(0, len(df_list_fix))])
    print('create df_list')

    basepath, ext = os.path.splitext(os.path.basename(__file__))
    now = dt.datetime.now().strftime('%Y%m%d')
    oldpath = 'data_{}_sp_{}.csv'.format(basepath, now)

    response = HttpResponse(content_type='text/csv; charset=UTF-8-sig')
    response['Content-Disposition'] = 'attachment; filename={}'.format(oldpath)
    df_fix.to_csv(path_or_buf=response, float_format='%.2f', decimal=",")

    sleep(1)
    driver.quit()

    return response
    # return render(request, 'scr/garage_hp.html')


