from django.urls import path
from . import views

app_name = 'grg_gn_sp'

urlpatterns = [
    path('', views.Index.as_view(), name="index"),
    path('garage/', views.Garage.as_view(), name='garage'),
    path('garage/gn/', views.grg_gn_sp, name='grg_gn_sp'),
]
