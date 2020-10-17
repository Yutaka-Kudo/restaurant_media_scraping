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
]
