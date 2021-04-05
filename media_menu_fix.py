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


driver = webdriver.Chrome(chrome_options=options)

# xlsxからーーーーーーーー
df = pd.read_csv('/users/yutakakudo/downloads/灯篭ドリンク.csv',header=None)

# ユビレジーーーーーーーーーーーーー
driver.get('https://ubiregi.com/a/')

id = "tourou"
pw = "tourou130"

driver.find_element_by_id('loginEmail').send_keys(id)
driver.find_element_by_id('loginPassword').send_keys(pw+Keys.ENTER)


def check_tax(li: list):
    for i, v in enumerate(li):
        if not v == "税込":
            print("税込じゃない")
            print(i)


def check_len(list1, list2, list3):
    len1, len2, len3 = len(list1), len(list2), len(list3)
    ave = (len1+len2+len3)/3
    if not ave == len1:
        print("長さが違う")


soup = BeautifulSoup(driver.page_source, 'html.parser')
item_name_list = [s.text.split('/')[-1] for s in soup.select('span.item-name')]
tax_type_list = [s.text for s in soup.select('span.is-tax-type')]
check_tax(tax_type_list)
price_list = [s.text for s in soup.select('td.is-price')]
check_len(item_name_list, tax_type_list, price_list)
df = pd.DataFrame({"名前": item_name_list, "tax": tax_type_list, "price": price_list})
df["カテゴリ"] = "つまみ"

soup = BeautifulSoup(driver.page_source, 'html.parser')
item_name_list = [s.text.split('/')[-1] for s in soup.select('span.item-name')]
tax_type_list = [s.text for s in soup.select('span.is-tax-type')]
check_tax(tax_type_list)
price_list = [s.text for s in soup.select('td.is-price')]
check_len(item_name_list, tax_type_list, price_list)
df2 = pd.DataFrame({"名前": item_name_list, "tax": tax_type_list, "price": price_list})
df2["カテゴリ"] = "料理"


soup = BeautifulSoup(driver.page_source, 'html.parser')
item_name_list = [s.text.split('/')[-1] for s in soup.select('span.item-name')]
tax_type_list = [s.text for s in soup.select('span.is-tax-type')]
check_tax(tax_type_list)
price_list = [s.text for s in soup.select('td.is-price')]
check_len(item_name_list, tax_type_list, price_list)
df3 = pd.DataFrame({"名前": item_name_list, "tax": tax_type_list, "price": price_list})
df3["カテゴリ"] = "甘味"

df_r = pd.concat([df, df2, df3])


driver.switch_to.window(driver.window_handles[0])
driver.switch_to.window(driver.window_handles[2])

tumami_df = df_r[df_r["カテゴリ"] == "つまみ"]
ryouri_df = df_r[df_r["カテゴリ"] == "料理"]
# ーーーーーーーーーーーーーーーユビレジ

# ぐるーーーーーーーーーーーーーーーーーーー
def get_elem_gn(i):
    items = driver.find_elements_by_class_name('tab__panel.is-active')[i:] # メニュー名と解説文
    items[0].find_elements_by_class_name('textarea__main')[0].click()
    sleep(0.5)
    items[0].find_elements_by_class_name('textarea__main')[1].click()
    sleep(0.5)
    items[0].find_element_by_class_name('input-text__main.is-auto.is-right').click() # 値段記入欄
    return items

items = get_elem_gn(0)

# 全体取得ーーーー
names, descriptions, prices = [],[],[]
for elem in items:
    names.append(elem.find_elements_by_class_name('textarea__main')[0].get_attribute('value'))
    descriptions.append(elem.find_elements_by_class_name('textarea__main')[1].get_attribute('value'))
    prices.append(elem.find_element_by_class_name('input-text__main.is-auto.is-right').get_attribute('value'))
if len(names) == len(descriptions) == len(prices):
    print(f'length OK {len(names)}')
else:
    print('lenあってない')


df = pd.DataFrame({"names":names,"desc": descriptions,"price": prices})
df.to_csv('pricechange_garage_gn_drink.csv')
df = pd.read_csv('pricechange_garage_gn_drink.csv')
df = df.fillna({"desc":"","price":0})
names = [i for i in df["names"].values]
descriptions = [i for i in df["desc"].values]
prices = [round(i) for i in df["price"].values]
prices = list(map(lambda x: "" if x == 0 else x, prices)) # 値段に空白をもたせたいとき

err_list = []
# 全体入力ーーーーーー
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
print(err_list)



#名前と値段まとめて処理用
for i, v in enumerate(df.itertuples()):
    menu_name_eles[i*2].clear()
    menu_name_eles[i*2].send_keys(v[1])
    menu_name_eles[i*2+1].clear()
    price_eles[i].clear()
    price_eles[i].send_keys(v[3][1:])
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")  # これないと読めない


# 現メニュー名集めてCSV化ーーーーーーーーーーー
menu_name_eles = driver.find_elements_by_class_name('textarea__main')[6:] # メニュー名と解説文
menu_name_eles[2].click() #試し
current_menu_list = []
for i in range(len(menu_name_eles)):
    try:
        current_menu_list.append(menu_name_eles[i*2].get_attribute('value'))
    except:
        pass
# 値段用ーーーーーーーーーーー
price_eles = driver.find_elements_by_class_name('input-text__main.is-auto.is-right')[::3][29:60] # 値段記入欄
price_eles[-1].click()
current_menu_list = []
for i in range(len(price_eles)):
    try:
        current_menu_list.append(price_eles[i].get_attribute('value'))
    except:
        pass

pd.DataFrame(current_menu_list).to_csv('pricechange_fesdrink2.csv')
df_fixprice = pd.read_csv('pricechange_fesdrink2.csv')
df_fixprice["0"]
df_fixprice.drop(38,inplace=True)
li = [round(i) for i in df_fixprice["0"].values]

#値段挿入ーーーーーー
for i,v in enumerate(li):
    price_eles[i].clear()
    debug(i)
    price_eles[i].send_keys(v)
    debug(i)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")  # これないと読めない
    print('down')

#ーーーーーーーーーーーーーーーぐる


driver.switch_to.window(driver.window_handles[0])
driver.switch_to.window(driver.window_handles[1])
driver.switch_to.window(driver.window_handles[-1])
driver.switch_to.window(driver.window_handles[-2])

# たべーーーーーーーーーーーーーーーー
def get_elem_tb(i):
    name_eles = driver.find_elements_by_class_name('js-menu-input.js-menu-input-name.oc-textfield.menu-line__menu-input')[i:]
    name_eles[0].click()
    description_eles = driver.find_elements_by_class_name('js-menu-input.js-menu-input-description.oc-textfield.oc-textfield--full.oc-textfield--textarea.menu-category__textarea')[i:]
    sleep(0.5)
    description_eles[0].click()
    price_eles = driver.find_elements_by_class_name('js-menu-input.js-menu-input-price.oc-textfield.menu-line__price-input')[i:]
    sleep(0.5)
    price_eles[0].click()
    return name_eles, description_eles, price_eles

name_eles, description_eles, price_eles = get_elem_tb(0)

# 全体取得ーーー
names, descriptions, prices = [],[],[]
for i, v in enumerate(name_eles):
    names.append(name_eles[i].get_attribute('value'))
    descriptions.append(description_eles[i].get_attribute('value'))
    prices.append(price_eles[i].get_attribute('value'))
if len(names) == len(descriptions) == len(prices):
    print('length OK')
else:
    print('lenあってない')

# 全体入力ーーーーーー
for i, v in enumerate(name_eles):
    name_eles[i].clear()
    name_eles[i].send_keys(names[i])
    description_eles[i].clear()
    description_eles[i].send_keys(descriptions[i])
    price_eles[i].clear()
    price_eles[i].send_keys(prices[i])


df = pd.DataFrame({"names":names,"desc": descriptions,"price": prices})
df.to_csv('pricechange_wananakame_tb_drink.csv')
df = pd.read_csv('pricechange_wananakame_tb_drink.csv')
df = df.fillna("")
names = [i for i in df["names"].values]
descriptions = [i for i in df["desc"].values]
prices = [round(i) for i in df["price"].values]

# 値段入力ーーーーー
for i,elem in enumerate(price_eles):
    elem.clear()
    elem.send_keys(price_list[i])

#名前と値段まとめて処理用
for i, v in enumerate(df2.itertuples()):
    name_eles[i].clear()
    name_eles[i].send_keys(v[1])
    description_eles[i].clear()
    price_eles[i].clear()
    # price_eles[i].send_keys(v[3][1:])  # ユビレジデータから用
    price_eles[i].send_keys(v[2]) # エクセルデータから用
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")  # これないと読めない

# ドリンク
df2 = df[df[2] == "ビール"]
df2 = df[df[2] == "サワー"]
df2 = df[df[2] == "果実酒"]
df2 = df[df[2] == "ウイスキー"]
df2 = df[df[2] == "ソフト"]


#ーーーーーーーーーーーーーーたべ



driver.switch_to.window(driver.window_handles[0])
driver.switch_to.window(driver.window_handles[1])
driver.switch_to.window(driver.window_handles[2])
driver.switch_to.window(driver.window_handles[-1])



#HPーーーーーーーーーーーーーーー
def get_elem_hp(i, where=""):
    if where == "food":
        items = driver.find_elements_by_class_name('item.jscSortItem.tableSort')[i:]
        exclude = driver.find_elements_by_class_name('item.jscSortItem.tableSort.disable') # 除外対象
    elif where == "drink":
        items = driver.find_elements_by_class_name('item.jscSortItem.tableSort')[i:]
        exclude = driver.find_elements_by_class_name('item.jscSortItem.tableSort.disable') # 除外対象
    elif where == "lunch":
        items = driver.find_elements_by_class_name('item.tableSort')[i:] # ランチ
        exclude = driver.find_elements_by_class_name('item.disable.tableSort') # 除外対象
    try:
        for e in exclude:
            items.remove(e)
    except:
        pass
    items[0].find_element_by_class_name('textarea.fitTextArea').click()
    return items


items = get_elem_hp(0,"food")[:-3]
items = get_elem_hp(0,"drink")
items = get_elem_hp(15,"lunch")

actions = webdriver.ActionChains(driver)
actions.move_to_element(items[-1]).perform() # ホバー

# 全体取得ーーーーーー
def get_all_hp():
    names, descriptions, prices = [],[],[]
    for elem in items: # 1アイテムごとに回すかんじ
        name = elem.find_elements_by_class_name('textarea.fitTextArea')[0].get_attribute('value') #名
        names.append(name)
        description = elem.find_elements_by_class_name('textarea.fitTextArea')[1].get_attribute('value')
        descriptions.append(description)
        price = elem.find_element_by_class_name('text.setMenuPrice.jscSetMenuPriceTxt').get_attribute('value') #値段
        prices.append(price)
        print(name,description,price)
        if not elem.find_element_by_class_name('jscTaxCheckBox').is_selected():
            elem.find_element_by_class_name('jscTaxCheckBox').click() #税込チェック
    if len(names) == len(descriptions) == len(prices):
        print('length OK')
    else:
        print('lenあってない')
    return names, descriptions, prices

names, descriptions, prices = get_all_hp()

df = pd.DataFrame({"names":names,"desc": descriptions,"price": prices})
df.to_csv('pricechange_garage_hp_food.csv')
df = pd.read_csv('pricechange_garage_hp_food.csv')
df = df.fillna("")
names = [i for i in df["names"].values]
descriptions = [i for i in df["desc"].values]
prices = [round(i) for i in df["price"].values]

# 全体入力ーーーーーー
for i,elem in enumerate(items):
    elem.find_elements_by_class_name('textarea.fitTextArea')[0].clear() #名
    elem.find_elements_by_class_name('textarea.fitTextArea')[0].send_keys(names[i]) #名
    description = elem.find_elements_by_class_name('textarea.fitTextArea')[1].clear()
    description = elem.find_elements_by_class_name('textarea.fitTextArea')[1].send_keys(descriptions[i])
    elem.find_element_by_class_name('jscSetMenuPriceCheck').click() # 料金を指定
    elem.find_element_by_class_name('text.setMenuPrice.jscSetMenuPriceTxt').clear()
    elem.find_element_by_class_name('text.setMenuPrice.jscSetMenuPriceTxt').send_keys(prices[i])




# ーーーーーーーーーーーーーーーーHP

driver.switch_to.window(driver.window_handles[0])
driver.switch_to.window(driver.window_handles[1])
driver.switch_to.window(driver.window_handles[2])
driver.switch_to.window(driver.window_handles[-1])


# レッティーーーーーーーーーーーーーーー
edits = driver.find_elements_by_class_name('btn.btn-small.btn-primary.btn-block.send')[1:] # forループの一番下にも数字忘れずに
len(edits)
len(names)
edits[0].click()
for i,v in enumerate(edits):
# for i,v in enumerate(edits,11):
    edits[i].click()
    driver.find_element_by_id('inputTitle').clear()
    driver.find_element_by_id('inputTitle').send_keys(names[i])
    driver.find_element_by_id('inputPrice').clear()
    driver.find_element_by_id('inputPrice').send_keys(prices[i])
    driver.find_element_by_class_name('btn.btn-primary').click()
    sleep(1)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") # これないと読めない
    edits = driver.find_elements_by_class_name('btn.btn-small.btn-primary.btn-block.send')[1:] # ここも！

# ーーーーーーーーーーーーーーーーーレッティー