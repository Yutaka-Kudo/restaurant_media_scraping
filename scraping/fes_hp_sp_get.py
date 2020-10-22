from .models import Fes_hp_sp_scrape
from django_pandas.io import read_frame
import datetime as dt
import pandas as pd
import os
from django.http import HttpResponse
from . import views
def fes_hp_sp_get(request):
    # month_keyでクエリセット
    # qs = Fes_hp_sp_scrape.objects.all()
    qs = Fes_hp_sp_scrape.objects.filter(month_key=views.fes_query)

    # qs = Fes_hp_sp_scrape.objects.filter(date__gte=dt.date(
    #     2020, 9, 24), date__lte=dt.date(2020, 10, 19))
    # qs2 = Fes_hp_sp_scrape.objects.filter(date__gte=dt.date(
    #     2020, 8, 27), date__lte=dt.date(2020, 9, 23))

    df = read_frame(qs)
    # df2 = read_frame(qs2)

    # df_fix = pd.concat([df2, df])

    # now = dt.datetime.now().strftime('%Y%m%d')
    basepath, ext = os.path.splitext(os.path.basename(__file__))
    oldpath = 'data_{}_sp_{}.csv'.format(basepath, views.fes_query)

    response = HttpResponse(content_type='text/csv; charset=UTF-8-sig')
    response['Content-Disposition'] = 'attachment; filename={}'.format(oldpath)
    df.to_csv(path_or_buf=response, float_format='%.2f', decimal=",")

    return response