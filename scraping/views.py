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
# import os
import random
from django.http import HttpResponse, HttpResponseRedirect

# from django.shortcuts import render
# from .models import Scraping
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.urls import reverse

from .grg_hp import grg_hp_sp, grgHpSp
from .grg_gn import grg_gn_sp, grgGnSp
from .grg_tb import grg_tb_sp
from .fes_hp import fes_hp_sp
from .fes_gn import fes_gn_sp
from .fes_tb import fes_tb_sp
from .wana_hp import wana_hp_sp
from .wana_gn import wana_gn_sp
from .wana_tb import wana_tb_sp
from .toro_hp import toro_hp_sp
from .toro_gn import toro_gn_sp
from .toro_tb import toro_tb_sp
from rq import Queue
from worker import conn


def index(request):
    return render(request, "scr/index.html")

# class Index(TemplateView):
#     template_name = "scr/index.html"


def garage(request):
    return render(request, "scr/garage.html")


def fes(request):
    return render(request, "scr/fes.html")


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
