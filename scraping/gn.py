from numpy import true_divide
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# import chromedriver_binary
from time import sleep, time
import pandas as pd
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
# import itertools
import os
from django.http import HttpResponse, HttpResponseRedirect

# from django.shortcuts import render
from django.shortcuts import render, redirect
# from django.views.generic import TemplateView
# from django.urls import reverse


from scraping.site_package.driver_settings import options

from scraping import models,pwd,hp,tb


def latest_all(request):
    gn_sp(request, all=True)
    hp.hp_sp(request, all=True)
    tb.tb_sp(request, all=True)
    return HttpResponse('全店舗取得完了しましたーー！！')


def capture(driver):
    n = datetime.now()
    FILENAME = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), f"static/images/screen{n.date()}{n.hour}{n.minute}.png")
    w = driver.execute_script('return document.body.scrollWidth;')
    h = driver.execute_script('return document.body.scrollHeight;')
    driver.set_window_size(w, h)
    driver.save_screenshot(FILENAME)

def gn_sp(request, all: bool = False):
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
            capture(driver)
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
            capture(driver)
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
            capture(driver)
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
            capture(driver)
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
                sleep(3) # これ絶対ひつよう
                df_list = pd.read_html(driver.page_source)
                df = df_list[0]

            except Exception:
                capture(driver)
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
                capture(driver)
                driver.quit()
                raise Exception('df fix NG')

            print('create df_list')

            month = df.index.astype(str)
            month_key = month[0][:7]  # 最初だけ month_key用

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
                        "month_key": month_key,
                    }
                )
        # PC
        try:
            sleep(2)
            elem = driver.find_element_by_xpath("//a[text()='PC']")
            print('PC btn catch!')
        except Exception:
            capture(driver)
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
                sleep(3) # これ絶対ひつよう
                df_list = pd.read_html(driver.page_source)
                df = df_list[0]

            except Exception:
                capture(driver)
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
                capture(driver)
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
            capture(driver)
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
                sleep(3) # これ絶対ひつよう
                df_list = pd.read_html(driver.page_source)
                df = df_list[0]

            except Exception:
                capture(driver)
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
                capture(driver)
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
                sleep(3)
                df = pd.read_html(driver.page_source)[0]
            except Exception:
                capture(driver)
                driver.quit()
                raise Exception('データ収集エラー2')

            try:
                df = df.T.reset_index(level=0, drop=True).T
                df = df.drop([df.index[-1],df.index[-2],df.index[-3]])
                df.set_index(df.columns[0], inplace=True)
                df.index = df.index.str.rstrip('(月火水木金土日)')
                df.index = pd.to_datetime(df.index, format='%Y/%m/%d')
            except Exception:
                capture(driver)
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

    context = {
        "start_year":start_year,
        "end_year": end_year,
        "start_month":start_month,
        "end_month":end_month,
    }

    return render(request, "scr/dev.html", context)






# # 手動用---------------ーーーーーーーーーーーー
# def replace_tax():
#     user_name = pwd.fgi
#     pw = pwd.fgp
#     user_name = pwd.ggi
#     pw = pwd.ggp
#     user_name = pwd.tgi
#     pw = pwd.tgp
#     user_name = pwd.wgi
#     pw = pwd.wgp
#     user_name = pwd.wngi
#     pw = pwd.wngp

#     driver = webdriver.Chrome(chrome_options=options)
#     driver.get("https://pro.gnavi.co.jp/")
#     id_input = driver.find_element_by_id("loginID").send_keys(user_name)
#     pw_input = driver.find_element_by_id('input_password').send_keys(pw)
#     pw_input.submit()


#     folist = driver.find_element_by_link_text("詳細").click()
#     folist = driver.find_element_by_class_name("menu-add__buttons")
#     folist = driver.find_elements_by_xpath("//input[@type='number']")
#     for fo in folist:
#         if fo.get_attribute('value'):
#             new_price = round(int(fo.get_attribute('value'))*1.1)
#             fo.clear()
#             fo.send_keys(new_price)



#     btn = driver.find_elements_by_class_name('menu-add__buttons')
#     btn[5].find_elements_by_link_text("詳細")[0].click()
#     for b in btn:
#         if kk.find_elements_by_link_text("詳細"):
#             print(777)

#     kk = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[2]/div/div/div[2]/div[2]/div[6]/div[1]/ul[2]/li[1]/a')
#     folist = driver.find_elements_by_link_text("詳細")
#     folist[0].click()
#     for f in folist:
#         f.click()



# def iii():
#     driver.find_element_by_class_name('switch-label').click()
#     driver.find_elements_by_class_name('radio__icon')[2].click()
#     driver.find_elements_by_class_name('button--large-primary')[1].click()


# iii() 


# # フードページ 〜詳細〜

# syousai = driver.find_elements_by_link_text('詳細')
# for num, sy in enumerate(syousai):
#     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") # これないと読めない
#     # sleep(1)
#     try:
#         sy.click()
#         print(num)
#         sleep(1)
#         oldprice = driver.find_element_by_xpath('/html/body/div[1]/div[3]/div[1]/div/div/div/div/div[3]/div/div[2]/div/div/div/div[1]/div[1]/div[3]/div/span[1]/span/input').get_attribute('value')
#         nuki = driver.find_element_by_xpath('/html/body/div[1]/div[3]/div[1]/div/div/div/div/div[3]/div/div[2]/div/div/div/div[1]/div[1]/div[1]/div/span[1]/span/input')
#         nukivalue = nuki.get_attribute('value')
#         if nukivalue == '':
#             driver.find_element_by_class_name('switch-label').click()
#             # sleep(1)
#             driver.find_elements_by_class_name('radio__icon')[2].click()
#             sleep(1)
#             # nuki = driver.find_element_by_xpath('/html/body/div[1]/div[3]/div[1]/div/div/div/div/div[3]/div/div[2]/div/div/div/div[1]/div[1]/div[1]/div/span[1]/span/input')
#             nuki.clear()
#             # sleep(1)
#             nuki.send_keys(oldprice)
#             # sleep(1)
#             driver.find_elements_by_class_name('button--large-primary')[1].click()
#             sleep(1)
#         else:
#             # driver.find_element_by_class_name('modal__close').click()
#             # sleep(1)

#             # もともと税抜き表示の場合ーーーーーーーーー
#             driver.find_element_by_class_name('switch-label').click()
#             driver.find_elements_by_class_name('radio__icon')[2].click()
#             driver.find_elements_by_class_name('button--large-primary')[1].click()
#             sleep(1)
#     except:
#         pass










# i = driver.find_element_by_class_name("textarea__main is-center")

# for i in folist:
# def addtax():
#     value = i.get_attribute('value')
#     index_num_list = [n for n,v in enumerate(value) if v == "円"]
#     if index_num_list:
#         for position in reversed(index_num_list):
#             st_posi = position-1
#             try:
#                 while type(int(value[st_posi])) == int:
#                     st_posi -= 1
#                     if value[st_posi] == ",":
#                         st_posi -= 1
#             except:
#                 old_price = value[st_posi+1:position].replace(',','')
#                 # print(old_price)
#                 new_price = (int(old_price)*1.08)
#                 # print(new_price)
#                 new_sentence = "(税込{:,.0f}円)".format(new_price)
#                 # print(new_sentence)
#                 value = value[:position+1]+new_sentence+value[position+1:]
#         print(value)
#         i.clear()
#         i.send_keys(value)

# i = driver.find_element_by_xpath('//*[@id="menu_text"]')
# addtax()









# # retty-----------------
#     driver.get('https://owner.retty.me/')
#     driver.find_element_by_id("inputMail").send_keys('questa_doi@yahoo.co.jp')
#     driver.find_element_by_id("inputPassword").send_keys('questa130')
#     driver.find_element_by_name("submit").click()


#     # i = driver.find_element_by_xpath("/html/body/div[3]/div[3]/div[1]/div/div/form/div[1]/table/tbody/tr[2]/td/div/div/textarea")

#     # メニューーーーーーー
#     fo = driver.find_elements_by_link_text("編集")
#     for i in range(len(fo)):
#         driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") # これないと読めない
#         sleep(1)
#         fo[i].click()
#         sleep(1.5)
#         inp = driver.find_element_by_id('inputPrice')
#         menuname = driver.find_element_by_id('inputTitle')
#         addtax(menuname)
#         try:
#             new_price = round(int(inp.get_attribute('value'))*1.1)
#             # if inp.get_attribute('value'):
#             inp.clear()
#             inp.send_keys(new_price)
#         except:
#             pass
#         driver.find_element_by_class_name('btn-primary').click()
#         print(i)
#         sleep(1.5)
#         fo = driver.find_elements_by_link_text("編集")





#     # for target in folist:
#     # def addtax():
#     def addtax(target):
#         value = target.get_attribute('value')
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
#             target.clear()
#             target.send_keys(value)

#     addtax()


#     target = driver.find_element_by_name('course_name')
#     addtax()
#     target = driver.find_element_by_id('appealPointInput')
#     addtax()

