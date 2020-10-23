# from selenium import webdriver
# from selenium.webdriver.support.select import Select
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# import chromedriver_binary
# from time import sleep
# import pandas as pd
# import datetime as dt
# import itertools
# import os
# import random
# from django.http import HttpResponse, HttpResponseRedirect

# from django.shortcuts import render
# from .models import Scraping
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.urls import reverse

from .grg_hp import grg_hp_sp
from .grg_gn import grg_gn_sp
from .grg_tb import grg_tb_sp
from .fes_hp import fes_hp_sp
# from .fes_hp_sp_get import fes_hp_sp_get
from .fes_gn import fes_gn_sp
from .fes_tb import fes_tb_sp
from .wana_hp import wana_hp_sp
from .wana_gn import wana_gn_sp
from .wana_tb import wana_tb_sp
from .toro_hp import toro_hp_sp
from .toro_gn import toro_gn_sp
from .toro_tb import toro_tb_sp

from django_pandas.io import read_frame
import datetime as dt
import pandas as pd
import os
from django.http import HttpResponse
from .models import (Fes_hp_sp_scrape,
                     Fes_gn_sp_scrape,
                     Fes_tb_sp_scrape,
                     Grg_hp_sp_scrape,
                     Grg_gn_sp_scrape,
                     Grg_tb_sp_scrape,
                     Toro_hp_sp_scrape,
                     Toro_gn_sp_scrape,
                     Toro_tb_sp_scrape,
                     Wana_hp_sp_scrape,
                     Wana_gn_sp_scrape,
                     Wana_tb_sp_scrape,
                     )


def index(request):
    return render(request, "scr/index.html")

# class Index(TemplateView):
#     template_name = "scr/index.html"


def dev(request):
    return render(request, 'scr/dev.html')


def garage(request):
    return render(request, "scr/garage.html")


def grg_gn_sp_get(request):
    fes_query = request.GET.get('q')

    # month_keyでクエリセット
    qs = Grg_gn_sp_scrape.objects.filter(month_key=fes_query)
    print(fes_query)

    df = read_frame(qs, fieldnames=["date", "week", "total", "top",
                                    "menu", "seat", "photo", "commitment", "map", "coupon", "reserve"])
    df.columns = ['日にち', "曜日", "合計", '店舗トップ', 'メニュー',
                  '席・個室・貸切', '写真', 'こだわり', '地図', 'クーポン', '予約']

    basepath, ext = os.path.splitext(os.path.basename(__file__))
    oldpath = 'data_grg_gn_sp_{}.csv'.format(fes_query)

    response = HttpResponse(content_type='text/csv; charset=UTF-8-sig')
    response['Content-Disposition'] = 'attachment; filename={}'.format(oldpath)
    df.to_csv(path_or_buf=response, index=False, float_format='%.2f', decimal=",")

    return response


def grg_hp_sp_get(request):
    fes_query = request.GET.get('q')

    # month_keyでクエリセット
    qs = Grg_hp_sp_scrape.objects.filter(month_key=fes_query)
    print(fes_query)

    df = read_frame(qs, fieldnames=["date", "week", "pv_all_sp", "pv_top_sp", "pv_coupon_sp", "cvr_sp",
                                    "tell_sp", "reserve_sp", "reserve_hp", "reserve_homepage", "day_over_day_changes"])
    df.columns = ["日付", "曜日", "店舗総PV（SP）", "店舗TOP PV（SP）", "クーポンページPV（SP）",
                  "CVR（SP）", "電話件数（SP）", "予約件数（SP）", "予約件数（ホットペッパー）", "予約件数（ホームページ）", "前日比"]

    basepath, ext = os.path.splitext(os.path.basename(__file__))
    oldpath = 'data_grg_hp_sp_{}.csv'.format(fes_query)

    response = HttpResponse(content_type='text/csv; charset=UTF-8-sig')
    response['Content-Disposition'] = 'attachment; filename={}'.format(oldpath)
    df.to_csv(path_or_buf=response, index=False, float_format='%.2f', decimal=",")

    return response


def grg_tb_sp_get(request):
    fes_query = request.GET.get('q')

    # month_keyでクエリセット
    qs = Grg_tb_sp_scrape.objects.filter(month_key=fes_query)
    print(fes_query)

    df = read_frame(qs, fieldnames=["date", "week", "top", "photo", "photo_info",
                                    "rating", "menu", "map", "coupon", "p_coupon", "seat", "other", "total"])
    df.columns = ["日付", "曜日", "店舗トップ", "写真一覧", "写真詳細", "口コミ・評価",
                  "メニュー", "お店地図", "クーポン", "プレミアムクーポン", "座席情報", "その他", "店舗全体（合計）"]

    basepath, ext = os.path.splitext(os.path.basename(__file__))
    oldpath = 'data_grg_tb_sp_{}.csv'.format(fes_query)

    response = HttpResponse(content_type='text/csv; charset=UTF-8-sig')
    response['Content-Disposition'] = 'attachment; filename={}'.format(oldpath)
    df.to_csv(path_or_buf=response, index=False, float_format='%.2f', decimal=",")

    return response


def fes(request):
    fes_query = request.GET.get('q')
    print(fes_query)
    return render(request, "scr/fes.html", {'fes_query': fes_query})


def fes_hp_sp_get(request):
    fes_query = request.GET.get('q')

    # month_keyでクエリセット
    # qs = Fes_hp_sp_scrape.objects.all()
    qs = Fes_hp_sp_scrape.objects.filter(month_key=fes_query)
    print(fes_query)

    # qs = Fes_hp_sp_scrape.objects.filter(date__gte=dt.date(
    #     2020, 9, 24), date__lte=dt.date(2020, 10, 19))
    # qs2 = Fes_hp_sp_scrape.objects.filter(date__gte=dt.date(
    #     2020, 8, 27), date__lte=dt.date(2020, 9, 23))

    df = read_frame(qs, fieldnames=["date", "week", "pv_all_sp", "pv_top_sp", "pv_coupon_sp", "cvr_sp",
                                    "tell_sp", "reserve_sp", "reserve_hp", "reserve_homepage", "day_over_day_changes"])
    df.columns = ["日付", "曜日", "店舗総PV（SP）", "店舗TOP PV（SP）", "クーポンページPV（SP）",
                  "CVR（SP）", "電話件数（SP）", "予約件数（SP）", "予約件数（ホットペッパー）", "予約件数（ホームページ）", "前日比"]

    # df2 = read_frame(qs2)

    # df_fix = pd.concat([df2, df])

    # now = dt.datetime.now().strftime('%Y%m%d')
    # basepath, ext = os.path.splitext(os.path.basename(__file__))
    oldpath = 'data_fes_hp_sp_{}.csv'.format(fes_query)

    response = HttpResponse(content_type='text/csv; charset=UTF-8-sig')
    response['Content-Disposition'] = 'attachment; filename={}'.format(oldpath)
    df.to_csv(path_or_buf=response, index=False, float_format='%.2f', decimal=",")

    return response


def fes_gn_sp_get(request):
    fes_query = request.GET.get('q')

    # month_keyでクエリセット
    qs = Fes_gn_sp_scrape.objects.filter(month_key=fes_query)
    print(fes_query)

    df = read_frame(qs, fieldnames=["date", "week", "total", "top",
                                    "menu", "seat", "photo", "commitment", "map", "coupon", "reserve"])
    df.columns = ['日にち', "曜日", "合計", '店舗トップ', 'メニュー',
                  '席・個室・貸切', '写真', 'こだわり', '地図', 'クーポン', '予約']

    basepath, ext = os.path.splitext(os.path.basename(__file__))
    oldpath = 'data_fes_gn_sp_{}.csv'.format(fes_query)

    response = HttpResponse(content_type='text/csv; charset=UTF-8-sig')
    response['Content-Disposition'] = 'attachment; filename={}'.format(oldpath)
    df.to_csv(path_or_buf=response, index=False, float_format='%.2f', decimal=",")

    return response


def fes_tb_sp_get(request):
    fes_query = request.GET.get('q')

    # month_keyでクエリセット
    qs = Fes_tb_sp_scrape.objects.filter(month_key=fes_query)
    print(fes_query)

    df = read_frame(qs, fieldnames=["date", "week", "top", "photo", "photo_info",
                                    "rating", "menu", "map", "coupon", "p_coupon", "seat", "other", "total"])
    df.columns = ["日付", "曜日", "店舗トップ", "写真一覧", "写真詳細", "口コミ・評価",
                  "メニュー", "お店地図", "クーポン", "プレミアムクーポン", "座席情報", "その他", "店舗全体（合計）"]

    basepath, ext = os.path.splitext(os.path.basename(__file__))
    oldpath = 'data_fes_tb_sp_{}.csv'.format(fes_query)

    response = HttpResponse(content_type='text/csv; charset=UTF-8-sig')
    response['Content-Disposition'] = 'attachment; filename={}'.format(oldpath)
    df.to_csv(path_or_buf=response, index=False, float_format='%.2f', decimal=",")

    return response


def wana(request):
    return render(request, "scr/wana_ichimoku.html")


def wana_gn_sp_get(request):
    fes_query = request.GET.get('q')

    # month_keyでクエリセット
    qs = Wana_gn_sp_scrape.objects.filter(month_key=fes_query)
    print(fes_query)

    df = read_frame(qs, fieldnames=["date", "week", "total", "top",
                                    "menu", "seat", "photo", "commitment", "map", "coupon", "reserve"])
    df.columns = ['日にち', "曜日", "合計", '店舗トップ', 'メニュー',
                  '席・個室・貸切', '写真', 'こだわり', '地図', 'クーポン', '予約']

    basepath, ext = os.path.splitext(os.path.basename(__file__))
    oldpath = 'data_wana_gn_sp_{}.csv'.format(fes_query)

    response = HttpResponse(content_type='text/csv; charset=UTF-8-sig')
    response['Content-Disposition'] = 'attachment; filename={}'.format(oldpath)
    df.to_csv(path_or_buf=response, index=False, float_format='%.2f', decimal=",")

    return response


def wana_hp_sp_get(request):
    fes_query = request.GET.get('q')

    # month_keyでクエリセット
    qs = Wana_hp_sp_scrape.objects.filter(month_key=fes_query)
    print(fes_query)

    df = read_frame(qs, fieldnames=["date", "week", "pv_all_sp", "pv_top_sp", "pv_coupon_sp", "cvr_sp",
                                    "tell_sp", "reserve_sp", "reserve_hp", "reserve_homepage", "day_over_day_changes"])
    df.columns = ["日付", "曜日", "店舗総PV（SP）", "店舗TOP PV（SP）", "クーポンページPV（SP）",
                  "CVR（SP）", "電話件数（SP）", "予約件数（SP）", "予約件数（ホットペッパー）", "予約件数（ホームページ）", "前日比"]

    basepath, ext = os.path.splitext(os.path.basename(__file__))
    oldpath = 'data_wana_hp_sp_{}.csv'.format(fes_query)

    response = HttpResponse(content_type='text/csv; charset=UTF-8-sig')
    response['Content-Disposition'] = 'attachment; filename={}'.format(oldpath)
    df.to_csv(path_or_buf=response, index=False, float_format='%.2f', decimal=",")

    return response


def wana_tb_sp_get(request):
    fes_query = request.GET.get('q')

    # month_keyでクエリセット
    qs = Wana_tb_sp_scrape.objects.filter(month_key=fes_query)
    print(fes_query)

    df = read_frame(qs, fieldnames=["date", "week", "top", "photo", "photo_info",
                                    "rating", "menu", "map", "coupon", "p_coupon", "seat", "other", "total"])
    df.columns = ["日付", "曜日", "店舗トップ", "写真一覧", "写真詳細", "口コミ・評価",
                  "メニュー", "お店地図", "クーポン", "プレミアムクーポン", "座席情報", "その他", "店舗全体（合計）"]

    basepath, ext = os.path.splitext(os.path.basename(__file__))
    oldpath = 'data_wana_tb_sp_{}.csv'.format(fes_query)

    response = HttpResponse(content_type='text/csv; charset=UTF-8-sig')
    response['Content-Disposition'] = 'attachment; filename={}'.format(oldpath)
    df.to_csv(path_or_buf=response, index=False, float_format='%.2f', decimal=",")

    return response


def toro(request):
    return render(request, "scr/toro.html")
# class Garage(TemplateView):
#     template_name = "scr/garage.html"


def toro_gn_sp_get(request):
    fes_query = request.GET.get('q')

    # month_keyでクエリセット
    qs = Toro_gn_sp_scrape.objects.filter(month_key=fes_query)
    print(fes_query)

    df = read_frame(qs, fieldnames=["date", "week", "total", "top",
                                    "menu", "seat", "photo", "commitment", "map", "coupon", "reserve"])
    df.columns = ['日にち', "曜日", "合計", '店舗トップ', 'メニュー',
                  '席・個室・貸切', '写真', 'こだわり', '地図', 'クーポン', '予約']

    basepath, ext = os.path.splitext(os.path.basename(__file__))
    oldpath = 'data_toro_gn_sp_{}.csv'.format(fes_query)

    response = HttpResponse(content_type='text/csv; charset=UTF-8-sig')
    response['Content-Disposition'] = 'attachment; filename={}'.format(oldpath)
    df.to_csv(path_or_buf=response, index=False, float_format='%.2f', decimal=",")

    return response


def toro_hp_sp_get(request):
    fes_query = request.GET.get('q')

    # month_keyでクエリセット
    qs = Toro_hp_sp_scrape.objects.filter(month_key=fes_query)
    print(fes_query)

    df = read_frame(qs, fieldnames=["date", "week", "pv_all_sp", "pv_top_sp", "pv_coupon_sp", "cvr_sp",
                                    "tell_sp", "reserve_sp", "reserve_hp", "reserve_homepage", "day_over_day_changes"])
    df.columns = ["日付", "曜日", "店舗総PV（SP）", "店舗TOP PV（SP）", "クーポンページPV（SP）",
                  "CVR（SP）", "電話件数（SP）", "予約件数（SP）", "予約件数（ホットペッパー）", "予約件数（ホームページ）", "前日比"]

    basepath, ext = os.path.splitext(os.path.basename(__file__))
    oldpath = 'data_toro_hp_sp_{}.csv'.format(fes_query)

    response = HttpResponse(content_type='text/csv; charset=UTF-8-sig')
    response['Content-Disposition'] = 'attachment; filename={}'.format(oldpath)
    df.to_csv(path_or_buf=response, index=False, float_format='%.2f', decimal=",")

    return response


def toro_tb_sp_get(request):
    fes_query = request.GET.get('q')

    # month_keyでクエリセット
    qs = Toro_tb_sp_scrape.objects.filter(month_key=fes_query)
    print(fes_query)

    df = read_frame(qs, fieldnames=["date", "week", "top", "photo", "photo_info",
                                    "rating", "menu", "map", "coupon", "p_coupon", "seat", "other", "total"])
    df.columns = ["日付", "曜日", "店舗トップ", "写真一覧", "写真詳細", "口コミ・評価",
                  "メニュー", "お店地図", "クーポン", "プレミアムクーポン", "座席情報", "その他", "店舗全体（合計）"]

    basepath, ext = os.path.splitext(os.path.basename(__file__))
    oldpath = 'data_toro_tb_sp_{}.csv'.format(fes_query)

    response = HttpResponse(content_type='text/csv; charset=UTF-8-sig')
    response['Content-Disposition'] = 'attachment; filename={}'.format(oldpath)
    df.to_csv(path_or_buf=response, index=False, float_format='%.2f', decimal=",")

    return response
