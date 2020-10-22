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
from .models import Fes_hp_sp_scrape
from .models import Fes_gn_sp_scrape
from .models import Fes_tb_sp_scrape


def index(request):
    return render(request, "scr/index.html")

# class Index(TemplateView):
#     template_name = "scr/index.html"


def dev(request):
    return render(request, 'scr/dev.html')


def garage(request):
    return render(request, "scr/garage.html")


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

    df = read_frame(qs)
    # df2 = read_frame(qs2)

    # df_fix = pd.concat([df2, df])

    # now = dt.datetime.now().strftime('%Y%m%d')
    # basepath, ext = os.path.splitext(os.path.basename(__file__))
    oldpath = 'data_fes_hp_sp_{}.csv'.format(fes_query)

    response = HttpResponse(content_type='text/csv; charset=UTF-8-sig')
    response['Content-Disposition'] = 'attachment; filename={}'.format(oldpath)
    df.to_csv(path_or_buf=response, float_format='%.2f', decimal=",")

    return response


def fes_gn_sp_get(request):
    fes_query = request.GET.get('q')

    # month_keyでクエリセット
    qs = Fes_gn_sp_scrape.objects.filter(month_key=fes_query)
    print(fes_query)

    df = read_frame(qs)

    basepath, ext = os.path.splitext(os.path.basename(__file__))
    oldpath = 'data_fes_gn_sp_{}.csv'.format(fes_query)

    response = HttpResponse(content_type='text/csv; charset=UTF-8-sig')
    response['Content-Disposition'] = 'attachment; filename={}'.format(oldpath)
    df.to_csv(path_or_buf=response, float_format='%.2f', decimal=",")

    return response


def fes_tb_sp_get(request):
    fes_query = request.GET.get('q')

    # month_keyでクエリセット
    qs = Fes_tb_sp_scrape.objects.filter(month_key=fes_query)
    print(fes_query)

    df = read_frame(qs)

    basepath, ext = os.path.splitext(os.path.basename(__file__))
    oldpath = 'data_fes_tb_sp_{}.csv'.format(fes_query)

    response = HttpResponse(content_type='text/csv; charset=UTF-8-sig')
    response['Content-Disposition'] = 'attachment; filename={}'.format(oldpath)
    df.to_csv(path_or_buf=response, float_format='%.2f', decimal=",")

    return response


def wana(request):
    return render(request, "scr/wana_ichimoku.html")


def toro(request):
    return render(request, "scr/toro.html")
# class Garage(TemplateView):
#     template_name = "scr/garage.html"


def garage_test(request):
    q = Queue(connection=conn)
    result = q.enqueue(garage, "request")
    return result
