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
# from django.shortcuts import render, redirect
# from django.views.generic import TemplateView
# from django.urls import reverse

from rq import Queue
from worker import conn

from .driver_settings import options


def fesGnSp(request):
    q = Queue(connection=conn)
    result = q.enqueue(fes_gn_sp, "request")
    return result


def fes_gn_sp(request):
    error_flg = False

    driver = webdriver.Chrome(chrome_options=options)
    # driver.set_window_size(1250, 1036)
    # driver.implicitly_wait(5)
    # wait = WebDriverWait(driver, 10)

    print('Browser is ready!')
    driver.set_page_load_timeout(3)

    try:
        url = "https://pro.gnavi.co.jp/"
        driver.get(url)
    except Exception:
        driver.execute_script("window.stop();")


    user_name = "ga42905"
    pw = "82527275"

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
        print('in btn chatch!')
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

    # PC　クリック
    # if error_flg is False:
    try:
        # sleep(1)
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
        # error_flg = True

    # In[17]:

    # 本番用
    # if error_flg is False:
    try:
        df_lists = []
        i = 2
        while i >= 0:
            # 月選択
            month_select_elem = driver.find_element_by_id('ym')
            month_select_object = Select(month_select_elem)
            month_select_object.select_by_index(i)
            sleep(1)

            # ここにデータ取得コードを。
            df_list = pd.read_html(driver.page_source)
            df_lists.append(df_list[0])
            
            print(i)

            i -= 1

    except Exception:
        # error_flg = True
        print('データ収集エラー')
        driver.quit()

    # In[18]:

    # In[19]:

    df_list_fix = []
    try:
        for df in df_lists:
            df.columns = ['日にち', "天気", "合計", '店舗トップ', 'メニュー',
                        '席・個室・貸切', '写真', 'こだわり', '地図', 'クーポン', '予約', 'その他']
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

            df_list_fix.append(df)
    except Exception:
        print('fix NG')
        driver.quit()

    # In[20]:

    df_fix = pd.concat([df_list_fix[i] for i in range(0, len(df_list_fix))])
    print('create df_list')

    basepath, ext = os.path.splitext(os.path.basename(__file__))
    now = dt.datetime.now().strftime('%Y%m%d')
    oldpath = 'data_{}_sp_{}.csv'.format(basepath, now)

    response = HttpResponse(content_type='text/csv; charset=UTF-8-sig')
    response['Content-Disposition'] = 'attachment; filename={}'.format(oldpath)
    df_fix.to_csv(path_or_buf=response, float_format='%.2f', decimal=",")

    driver.quit()

    return response
    # return render(request, "scr/index.html")
