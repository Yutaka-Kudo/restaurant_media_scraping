from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
# import chromedriver_binary
from bs4 import BeautifulSoup
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
from scraping import models, pwd, hp, tb
from devtools import debug
# 下に関数あるよ！！！！！！！！！！！！！！！！！

# def check_tax(li: list):
#     for i, v in enumerate(li):
#         if not v == "税込":
#             print("税込じゃない")
#             print(i)


# def check_len(list1, list2, list3):
#     len1, len2, len3 = len(list1), len(list2), len(list3)
#     ave = (len1+len2+len3)/3
#     if not ave == len1:
#         print("長さが違う")

# # ユビレジーーーーーーーーーーーーー
# driver.get('https://ubiregi.com/a/')
# id = "tourou"
# pw = "tourou130"
# driver.find_element_by_id('loginEmail').send_keys(id)
# driver.find_element_by_id('loginPassword').send_keys(pw+Keys.ENTER)

# soup = BeautifulSoup(driver.page_source, 'html.parser')
# item_name_list = [s.text.split('/')[-1] for s in soup.select('span.item-name')]
# tax_type_list = [s.text for s in soup.select('span.is-tax-type')]
# check_tax(tax_type_list)
# price_list = [s.text for s in soup.select('td.is-price')]
# check_len(item_name_list, tax_type_list, price_list)
# df = pd.DataFrame({"名前": item_name_list, "tax": tax_type_list, "price": price_list})
# df["カテゴリ"] = "つまみ"

# soup = BeautifulSoup(driver.page_source, 'html.parser')
# item_name_list = [s.text.split('/')[-1] for s in soup.select('span.item-name')]
# tax_type_list = [s.text for s in soup.select('span.is-tax-type')]
# check_tax(tax_type_list)
# price_list = [s.text for s in soup.select('td.is-price')]
# check_len(item_name_list, tax_type_list, price_list)
# df2 = pd.DataFrame({"名前": item_name_list, "tax": tax_type_list, "price": price_list})
# df2["カテゴリ"] = "料理"


# soup = BeautifulSoup(driver.page_source, 'html.parser')
# item_name_list = [s.text.split('/')[-1] for s in soup.select('span.item-name')]
# tax_type_list = [s.text for s in soup.select('span.is-tax-type')]
# check_tax(tax_type_list)
# price_list = [s.text for s in soup.select('td.is-price')]
# check_len(item_name_list, tax_type_list, price_list)
# df3 = pd.DataFrame({"名前": item_name_list, "tax": tax_type_list, "price": price_list})
# df3["カテゴリ"] = "甘味"

# df_r = pd.concat([df, df2, df3])


# driver.switch_to.window(driver.window_handles[0])
# driver.switch_to.window(driver.window_handles[2])

# tumami_df = df_r[df_r["カテゴリ"] == "つまみ"]
# ryouri_df = df_r[df_r["カテゴリ"] == "料理"]
# # ーーーーーーーーーーーーーーーユビレジ

# ぐるーーーーーーーーーーーーーーーーーーー
def get_elem_gn(start_elem_num: int):
    items = driver.find_elements_by_class_name('tab__panel.is-active')[start_elem_num:]  # メニュー名と解説文
    items[0].find_elements_by_class_name('textarea__main')[0].click()
    sleep(0.5)
    items[0].find_elements_by_class_name('textarea__main')[1].click()
    sleep(0.5)
    items[0].find_element_by_class_name('input-text__main.is-auto.is-right').click()  # 値段記入欄
    return items

# 全体取得ーーーー


def get_all_gn(items):
    names, descriptions, prices = [], [], []
    for elem in items:
        names.append(elem.find_elements_by_class_name('textarea__main')[0].get_attribute('value'))
        descriptions.append(elem.find_elements_by_class_name('textarea__main')[1].get_attribute('value'))
        prices.append(elem.find_element_by_class_name('input-text__main.is-auto.is-right').get_attribute('value'))
        print(elem.find_elements_by_class_name('textarea__main')[0].get_attribute('value'))
    if len(names) == len(descriptions) == len(prices):
        print(f'length OK {len(names)}')
    else:
        print('lenあってない')
    return names, descriptions, prices

# 全体入力ーーーーーー


def input_all_gn(items):
    err_list = []
    for i, elem in enumerate(items):
        elem.find_elements_by_class_name('textarea__main')[0].clear()
        elem.find_elements_by_class_name('textarea__main')[0].send_keys(names[i])
        elem.find_elements_by_class_name('textarea__main')[1].clear()
        elem.find_elements_by_class_name('textarea__main')[1].send_keys(descriptions[i])
        try:
            elem.find_element_by_class_name('input-text__main.is-auto.is-right').clear()
            elem.find_element_by_class_name('input-text__main.is-auto.is-right').send_keys(prices[i])
        except:
            err_list.append(names[i])
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")  # これないと読めない
    debug(err_list)
# ーーーーーーーーーーーーーーーぐる

# たべーーーーーーーーーーーーーーーー


def get_elem_tb(start_elem_num: int):
    name_eles = driver.find_elements_by_class_name('js-menu-input.js-menu-input-name.oc-textfield.menu-line__menu-input')[start_elem_num]
    name_eles[0].click()
    description_eles = driver.find_elements_by_class_name('js-menu-input.js-menu-input-description.oc-textfield.oc-textfield--full.oc-textfield--textarea.menu-category__textarea')[start_elem_num]
    sleep(0.5)
    description_eles[0].click()
    price_eles = driver.find_elements_by_class_name('js-menu-input.js-menu-input-price.oc-textfield.menu-line__price-input')[start_elem_num]
    sleep(0.5)
    price_eles[0].click()
    return name_eles, description_eles, price_eles

# 全体取得ーーー


def get_all_tb(name_eles, description_eles, price_eles):
    names, descriptions, prices = [], [], []
    for i, v in enumerate(name_eles):
        names.append(name_eles[i].get_attribute('value'))
        descriptions.append(description_eles[i].get_attribute('value'))
        prices.append(price_eles[i].get_attribute('value'))
    if len(names) == len(descriptions) == len(prices):
        print('length OK')
    else:
        print('lenあってない')
    return names, descriptions, prices

# 全体入力ーーーーーー


def input_all_tb(name_eles, description_eles, price_eles):
    for i, v in enumerate(name_eles):
        name_eles[i].clear()
        name_eles[i].send_keys(names[i])
        description_eles[i].clear()
        description_eles[i].send_keys(descriptions[i])
        price_eles[i].clear()
        price_eles[i].send_keys(prices[i])
# ーーーーーーーーーーーーーーたべ

# HPーーーーーーーーーーーーーーー


def get_elem_hp(start_elem_num: int, where=""):
    if where == "food":
        items = driver.find_elements_by_class_name('item.jscSortItem.tableSort')[start_elem_num:]
        exclude = driver.find_elements_by_class_name('item.jscSortItem.tableSort.disable')  # 除外対象
    elif where == "drink":
        items = driver.find_elements_by_class_name('item.jscSortItem.tableSort')[start_elem_num:]
        exclude = driver.find_elements_by_class_name('item.jscSortItem.tableSort.disable')  # 除外対象
    elif where == "lunch":
        items = driver.find_elements_by_class_name('item.tableSort')[start_elem_num:]  # ランチ
        exclude = driver.find_elements_by_class_name('item.disable.tableSort')  # 除外対象
    try:
        for e in exclude:
            items.remove(e)
    except:
        pass
    items[0].find_elements_by_class_name('textarea.fitTextArea')[0].click()
    sleep(0.5)
    items[0].find_elements_by_class_name('textarea.fitTextArea')[1].click()
    sleep(0.5)
    items[0].find_element_by_class_name('text.setMenuPrice.jscSetMenuPriceTxt').click()
    return items


def hover():
    actions = webdriver.ActionChains(driver)
    actions.move_to_element(items[-1]).perform()  # ホバー

# 全体取得ーーーーーー


def get_all_hp(items):
    names, descriptions, prices = [], [], []
    for elem in items:  # 1アイテムごとに回すかんじ
        name = elem.find_elements_by_class_name('textarea.fitTextArea')[0].get_attribute('value')  # 名
        names.append(name)
        description = elem.find_elements_by_class_name('textarea.fitTextArea')[1].get_attribute('value')
        descriptions.append(description)
        price = elem.find_element_by_class_name('text.setMenuPrice.jscSetMenuPriceTxt').get_attribute('value')  # 値段
        prices.append(price)
        print(name, description, price)
    if len(names) == len(descriptions) == len(prices):
        print('length OK')
    else:
        print('lenあってない')
    return names, descriptions, prices


def tax_checkbox_on(items):  # 税込チェック
    for elem in items:
        if not elem.find_element_by_class_name('jscTaxCheckBox').is_selected():
            elem.find_element_by_class_name('jscTaxCheckBox').click()

# 全体入力ーーーーーー


def input_all_hp(items):
    for i, elem in enumerate(items):
        elem.find_elements_by_class_name('textarea.fitTextArea')[0].clear()  # 名
        elem.find_elements_by_class_name('textarea.fitTextArea')[0].send_keys(names[i])  # 名
        description = elem.find_elements_by_class_name('textarea.fitTextArea')[1].clear()
        description = elem.find_elements_by_class_name('textarea.fitTextArea')[1].send_keys(descriptions[i])
        elem.find_element_by_class_name('jscSetMenuPriceCheck').click()  # 料金を指定
        elem.find_element_by_class_name('text.setMenuPrice.jscSetMenuPriceTxt').clear()
        elem.find_element_by_class_name('text.setMenuPrice.jscSetMenuPriceTxt').send_keys(prices[i])
# ーーーーーーーーーーーーーーーーHP

# レッティーーーーーーーーーーーーーーー


def get_elem_retty(start_elem_num):
    edits = driver.find_elements_by_class_name('btn.btn-small.btn-primary.btn-block.send')[start_elem_num:]  # forループの一番下にも数字忘れずに
    debug(len(edits))
    debug(len(names))
    edits[0].click()
    return edits


def input_retty(edits, start_elem_num: int):
    for i, v in enumerate(edits):
        # for i,v in enumerate(edits,11):
        edits[i].click()
        driver.find_element_by_id('inputTitle').clear()
        driver.find_element_by_id('inputTitle').send_keys(names[i])
        driver.find_element_by_id('inputPrice').clear()
        driver.find_element_by_id('inputPrice').send_keys(prices[i])
        driver.find_element_by_class_name('btn.btn-primary').click()
        sleep(1)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")  # これないと読めない
        edits = driver.find_elements_by_class_name('btn.btn-small.btn-primary.btn-block.send')[start_elem_num:]  # ここも！
# ーーーーーーーーーーーーーーーーーレッティー

# ここから上、先に読み込み！！！！！！！！！！！！！！！！！！！
# ここから上、先に読み込み！！！！！！！！！！！！！！！！！！！
# ここから上、先に読み込み！！！！！！！！！！！！！！！！！！！


driver = webdriver.Chrome(chrome_options=options)

driver.switch_to.window(driver.window_handles[0])
driver.switch_to.window(driver.window_handles[1])
driver.switch_to.window(driver.window_handles[-2])
driver.switch_to.window(driver.window_handles[-1])

# ぐるーーーーーーーーーーーーーーーーーーー
driver.get("https://pro.gnavi.co.jp/")
user_name_gn = pwd.fgi
pw_gn = pwd.fgp
user_name_gn = pwd.ggi
pw_gn = pwd.ggp
user_name_gn = pwd.tgi
pw_gn = pwd.tgp
user_name_gn = pwd.wgi
pw_gn = pwd.wgp
user_name_gn = pwd.wngi
pw_gn = pwd.wngp
driver.find_element_by_id("loginID").send_keys(user_name_gn)
driver.find_element_by_id('input_password').send_keys(pw_gn + Keys.ENTER)

items = get_elem_gn(start_elem_num=0)[:-1]
items[-1].find_element_by_class_name('textarea__main').click()  # 最後列の確認
names, descriptions, prices = get_all_gn(items=items)
input_all_gn(items=items)
# ーーーーーーーーーーーーーーーぐる

# たべーーーーーーーーーーーーーーーー
driver.get("https://ssl.tabelog.com/owner_account/login/")
driver.find_element_by_id('login_id').send_keys(pwd.tbi)
driver.find_element_by_id('password').send_keys(pwd.tbp + Keys.ENTER)

name_eles, description_eles, price_eles = get_elem_tb(start_elem_num=0)
names, descriptions, prices = get_all_tb(name_eles, description_eles, price_eles)
input_all_tb(name_eles, description_eles, price_eles)
# ーーーーーーーーーーーーーーたべ

# HPーーーーーーーーーーーーーーー
driver.get("https://www.cms.hotpepper.jp/CLN/login/")
driver.find_element_by_xpath("/html/body/div[2]/div/form/div/div[2]/table/tbody/tr[1]/td/input").send_keys(pwd.hpi)
driver.find_element_by_name('password').send_keys(pwd.hpp + Keys.ENTER)

items = get_elem_hp(start_elem_num=0, where="food")[:-3]  # 最下層の無駄な欄を除外
items = get_elem_hp(start_elem_num=0, where="drink")
items = get_elem_hp(start_elem_num=15, where="lunch")[:-1]  # 最下層の無駄な欄を除外
items[-1].find_element_by_class_name('textarea.fitTextArea').click()  # 最後列の確認
hover()  # ホバーもあるよ
names, descriptions, prices = get_all_hp(items=items)
tax_checkbox_on(items=items)  # 税込チェック
input_all_hp(items=items)
# ーーーーーーーーーーーーーーーーHP

# レッティーーーーーーーーーーーーーーー
start_elem_num = 0  # 最初に決める
edits = get_elem_retty(start_elem_num)  # editsのlenがnamesのlenより少なくならないように
input_retty(edits=edits, start_elem_num=start_elem_num)  # カテゴリ分けはこのあと手動で
# ーーーーーーーーーーーーーーーーーレッティー

# CSV処理ーーーーーーーーー
CSVname = "pricechange_garage_gn_drink.csv"  # 確認！！
df = pd.DataFrame({"names": names, "desc": descriptions, "price": prices})
df.to_csv(CSVname)  # このCSVを手動で修正入力

df = pd.read_csv(CSVname)
df = df.fillna("")
# df = df.fillna({"desc": "", "price": 0}) # 個別の処理 ぐるなびだっけ いらないっけ
names = [i for i in df["names"].values]
descriptions = [i for i in df["desc"].values]
prices = [round(i) for i in df["price"].values]
# prices = list(map(lambda x: "" if x == 0 else x, prices))  # 値段に空白をもたせたいとき  ぐるなびだっけ いらないっけ
