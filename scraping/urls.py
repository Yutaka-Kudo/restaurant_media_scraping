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
    # path('fes/', views.fes_tb_sp, name='fes_page'),
    # path('fes/gn/', views.fes_gn_sp, name='fes_gn_sp'),
    # path('fes/hp/', views.fes_hp_sp, name='fes_hp_sp'),
    # path('fes/tb/', views.fes_tb_sp, name='fes_tb_sp'),
]
