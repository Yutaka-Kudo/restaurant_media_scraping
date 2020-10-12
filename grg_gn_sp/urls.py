from django.urls import path
from . import views

app_name = 'grg_gn_sp'


urlpatterns = [
    path('', views.index, name="index"),
    path('garage/', views.garage, name='garage'),
    # path('garage/gn/', views.grg_gn_sp, name='grg_gn_sp'),
]
