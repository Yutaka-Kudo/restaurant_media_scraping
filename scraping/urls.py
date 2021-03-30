from django.urls import path
from scraping import views
from scraping import hp, gn, tb
# from . import grg_hp


app_name = 'scraping'


urlpatterns = [
    path('', views.index, name="index"),
    path('admin/', views.admin_scr, name='admin'),
    path('dev/', views.dev, name="dev"),

    path('gn', gn.gn_sp, name='gn_sp'),
    path('hp', hp.hp_sp, name='hp_sp'),
    path('tb', tb.tb_sp, name='tb_sp'),
    path('all', gn.latest_all, name='latest_all'),
    # path('<str:store>', views.store_page, name='store_page'),
    path('chart_GMB/<str:store>', views.chart_GMB, name='chart_GMB'),
    path('<str:store>/<str:media>', views.download_excel, name='download_excel'),
    path('<str:store>/<str:media>/chart', views.chart, name='chart'),
]
