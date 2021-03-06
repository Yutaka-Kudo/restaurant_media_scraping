from django.urls import path
from . import views
from scraping import hp, gn, tb
# from . import grg_hp


app_name = 'scraping'


urlpatterns = [
    path('', views.index, name="index"),
    path('admin/', views.admin_scr, name='admin'),

    path('dev/', views.dev, name="dev"),


    path('gn/', gn.gn_sp, name='gn_sp'),
    path('hp/', hp.hp_sp, name='hp_sp'),
    path('tb/', tb.tb_sp, name='tb_sp'),

    path('garage/', views.garage, name='garage_page'),
    path('garage/gn/get/', views.grg_gn_sp_get, name='grg_gn_sp_get'),
    path('garage/hp/get/', views.grg_hp_sp_get, name='grg_hp_sp_get'),
    path('garage/tb/get/', views.grg_tb_sp_get, name='grg_tb_sp_get'),
    path('fes/', views.fes, name='fes_page'),
    path('fes/gn/get/', views.fes_gn_sp_get, name='fes_gn_sp_get'),
    path('fes/hp/get/', views.fes_hp_sp_get, name='fes_hp_sp_get'),
    path('fes/tb/get/', views.fes_tb_sp_get, name='fes_tb_sp_get'),
    path('wana/', views.wana, name='wana_page'),
    path('wana/gn/get/', views.wana_gn_sp_get, name='wana_gn_sp_get'),
    path('wana/hp/get/', views.wana_hp_sp_get, name='wana_hp_sp_get'),
    path('wana/tb/get/', views.wana_tb_sp_get, name='wana_tb_sp_get'),
    path('toro/', views.toro, name='toro_page'),
    path('toro/gn/get', views.toro_gn_sp_get, name='toro_gn_sp_get'),
    path('toro/hp/get', views.toro_hp_sp_get, name='toro_hp_sp_get'),
    path('toro/tb/get', views.toro_tb_sp_get, name='toro_tb_sp_get'),
]
