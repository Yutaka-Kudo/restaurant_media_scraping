from django.urls import path
from . import views

app_name = 'grg'


urlpatterns = [
    path('', views.index, name="index"),
    path('garage/', views.garage, name='garage_page'),
    path('garage/gn/', views.grg_gn_sp, name='grg_gn_sp'),
    path('garage/hp/', views.grg_hp_sp, name='grg_hp_sp'),
]
