from django.urls import path
from . import views
from . import grg_hp


app_name = 'grg'


urlpatterns = [
    path('', views.index, name="index"),
    path('garage/', views.garage, name='garage_page'),
    path('garage/gn/', views.grgGnSp, name='grg_gn_sp'),
    path('garage/hp/', views.grgHpSp, name='grg_hp_sp'),
]
