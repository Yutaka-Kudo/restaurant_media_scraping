from django.urls import path
from . import views
from . import grg_hp


app_name = 'scraping'


urlpatterns = [
    path('', views.index, name="index"),
    path('garage/', views.garage, name='garage_page'),
    path('garage/gn/', views.grg_gn_sp, name='grg_gn_sp'),
    path('garage/hp/', views.grg_hp_sp, name='grg_hp_sp'),
    path('garage/tb/', views.grg_tb_sp, name='grg_tb_sp'),
    path('fes/', views.fes, name='fes_page'),
    path('fes/gn/', views.fes_gn_sp, name='fes_gn_sp'),
    path('fes/hp/', views.fes_hp_sp, name='fes_hp_sp'),
    path('fes/hp/get/', views.fes_hp_sp_get, name='fes_hp_sp_get'),
    path('fes/tb/', views.fes_tb_sp, name='fes_tb_sp'),
    path('wana/', views.wana, name='wana_page'),
    path('wana/gn/', views.wana_gn_sp, name='wana_gn_sp'),
    path('wana/hp/', views.wana_hp_sp, name='wana_hp_sp'),
    path('wana/tb/', views.wana_tb_sp, name='wana_tb_sp'),
    path('toro/', views.toro, name='toro_page'),
    path('toro/gn/', views.toro_gn_sp, name='toro_gn_sp'),
    path('toro/hp/', views.toro_hp_sp, name='toro_hp_sp'),
    path('toro/tb/', views.toro_tb_sp, name='toro_tb_sp'),
]
