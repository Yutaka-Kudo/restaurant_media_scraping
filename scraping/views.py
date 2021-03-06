from django.shortcuts import render, redirect

from django_pandas.io import read_frame
import os
from django.http import HttpResponse
from scraping import models


def index(request):
    return render(request, "scr/index.html")


def admin_scr(request):
    return redirect('/admin/')


def dev(request):
    return render(request, 'scr/dev.html')


def garage(request):
    return render(request, "scr/garage.html")


def grg_gn_sp_get(request):
    fes_query = request.GET.get('q')

    # month_keyでクエリセット
    qs = models.Grg_gn_sp_scrape.objects.filter(month_key=fes_query)
    print(fes_query)

    df = read_frame(qs, fieldnames=["date", "week", "total", "top",
                                    "menu", "seat", "photo", "commitment", "map", "coupon", "reserve"])
    df.columns = ['日にち', "曜日", "合計", '店舗トップ', 'メニュー',
                  '席・個室・貸切', '写真', 'こだわり', '地図', 'クーポン', '予約']

    basepath, ext = os.path.splitext(os.path.basename(__file__))
    oldpath = 'data_grg_gn_sp_{}.csv'.format(fes_query)

    response = HttpResponse(content_type='text/csv; charset=UTF-8-sig')
    response['Content-Disposition'] = 'attachment; filename={}'.format(oldpath)
    df.to_csv(path_or_buf=response, index=False, float_format='%.2f', decimal=",")

    return response


def grg_hp_sp_get(request):
    fes_query = request.GET.get('q')

    # month_keyでクエリセット
    qs = models.Grg_hp_sp_scrape.objects.filter(month_key=fes_query)
    print(fes_query)

    df = read_frame(qs, fieldnames=["date", "week", "pv_all_sp", "pv_top_sp", "pv_coupon_sp", "cvr_sp",
                                    "tell_sp", "reserve_sp", "reserve_hp", "reserve_homepage", "day_over_day_changes"])
    df.columns = ["日付", "曜日", "店舗総PV（SP）", "店舗TOP PV（SP）", "クーポンページPV（SP）",
                  "CVR（SP）", "電話件数（SP）", "予約件数（SP）", "予約件数（ホットペッパー）", "予約件数（ホームページ）", "前日比"]

    basepath, ext = os.path.splitext(os.path.basename(__file__))
    oldpath = 'data__{}.csv'.format(fes_query)

    response = HttpResponse(content_type='text/csv; charset=UTF-8-sig')
    response['Content-Disposition'] = 'attachment; filename={}'.format(oldpath)
    df.to_csv(path_or_buf=response, index=False, float_format='%.2f', decimal=",")

    return response


def grg_tb_sp_get(request):
    fes_query = request.GET.get('q')

    # month_keyでクエリセット
    qs = models.Grg_tb_sp_scrape.objects.filter(month_key=fes_query)
    print(fes_query)

    df = read_frame(qs, fieldnames=["date", "week", "top", "photo", "photo_info",
                                    "rating", "menu", "map", "coupon", "p_coupon", "seat", "other", "total"])
    df.columns = ["日付", "曜日", "店舗トップ", "写真一覧", "写真詳細", "口コミ・評価",
                  "メニュー", "お店地図", "クーポン", "プレミアムクーポン", "座席情報", "その他", "店舗全体（合計）"]

    basepath, ext = os.path.splitext(os.path.basename(__file__))
    oldpath = 'data_grg_tb_sp_{}.csv'.format(fes_query)

    response = HttpResponse(content_type='text/csv; charset=UTF-8-sig')
    response['Content-Disposition'] = 'attachment; filename={}'.format(oldpath)
    df.to_csv(path_or_buf=response, index=False, float_format='%.2f', decimal=",")

    return response


def fes(request):
    fes_query = request.GET.get('q')
    print(fes_query)
    return render(request, "scr/fes.html", {'fes_query': fes_query})


def fes_hp_sp_get(request):
    fes_query = request.GET.get('q')

    # month_keyでクエリセット
    # qs = models.Fes_hp_sp_scrape.objects.all()
    qs = models.Fes_hp_sp_scrape.objects.filter(month_key=fes_query)
    print(fes_query)

    # qs = Fes_hp_sp_scrape.objects.filter(date__gte=dt.date(
    #     2020, 9, 24), date__lte=dt.date(2020, 10, 19))
    # qs2 = Fes_hp_sp_scrape.objects.filter(date__gte=dt.date(
    #     2020, 8, 27), date__lte=dt.date(2020, 9, 23))

    df = read_frame(qs, fieldnames=["date", "week", "pv_all_sp", "pv_top_sp", "pv_coupon_sp", "cvr_sp",
                                    "tell_sp", "reserve_sp", "reserve_hp", "reserve_homepage", "day_over_day_changes"])
    df.columns = ["日付", "曜日", "店舗総PV（SP）", "店舗TOP PV（SP）", "クーポンページPV（SP）",
                  "CVR（SP）", "電話件数（SP）", "予約件数（SP）", "予約件数（ホットペッパー）", "予約件数（ホームページ）", "前日比"]

    # df2 = read_frame(qs2)

    # df_fix = pd.concat([df2, df])

    # now = dt.datetime.now().strftime('%Y%m%d')
    # basepath, ext = os.path.splitext(os.path.basename(__file__))
    oldpath = 'data_fes_hp_sp_{}.csv'.format(fes_query)

    response = HttpResponse(content_type='text/csv; charset=UTF-8-sig')
    response['Content-Disposition'] = 'attachment; filename={}'.format(oldpath)
    df.to_csv(path_or_buf=response, index=False, float_format='%.2f', decimal=",")

    return response


def fes_gn_sp_get(request):
    fes_query = request.GET.get('q')

    # month_keyでクエリセット
    qs = models.Fes_gn_sp_scrape.objects.filter(month_key=fes_query)
    print(fes_query)

    df = read_frame(qs, fieldnames=["date", "week", "total", "top",
                                    "menu", "seat", "photo", "commitment", "map", "coupon", "reserve"])
    df.columns = ['日にち', "曜日", "合計", '店舗トップ', 'メニュー',
                  '席・個室・貸切', '写真', 'こだわり', '地図', 'クーポン', '予約']

    basepath, ext = os.path.splitext(os.path.basename(__file__))
    oldpath = 'data_fes_gn_sp_{}.csv'.format(fes_query)

    response = HttpResponse(content_type='text/csv; charset=UTF-8-sig')
    response['Content-Disposition'] = 'attachment; filename={}'.format(oldpath)
    df.to_csv(path_or_buf=response, index=False, float_format='%.2f', decimal=",")

    return response


def fes_tb_sp_get(request):
    fes_query = request.GET.get('q')

    # month_keyでクエリセット
    qs = models.Fes_tb_sp_scrape.objects.filter(month_key=fes_query)
    print(fes_query)

    df = read_frame(qs, fieldnames=["date", "week", "top", "photo", "photo_info",
                                    "rating", "menu", "map", "coupon", "p_coupon", "seat", "other", "total"])
    df.columns = ["日付", "曜日", "店舗トップ", "写真一覧", "写真詳細", "口コミ・評価",
                  "メニュー", "お店地図", "クーポン", "プレミアムクーポン", "座席情報", "その他", "店舗全体（合計）"]

    basepath, ext = os.path.splitext(os.path.basename(__file__))
    oldpath = 'data_fes_tb_sp_{}.csv'.format(fes_query)

    response = HttpResponse(content_type='text/csv; charset=UTF-8-sig')
    response['Content-Disposition'] = 'attachment; filename={}'.format(oldpath)
    df.to_csv(path_or_buf=response, index=False, float_format='%.2f', decimal=",")

    return response


def wana(request):
    return render(request, "scr/wana_ichimoku.html")


def wana_gn_sp_get(request):
    fes_query = request.GET.get('q')

    # month_keyでクエリセット
    qs = models.Wana_gn_sp_scrape.objects.filter(month_key=fes_query)
    print(fes_query)

    df = read_frame(qs, fieldnames=["date", "week", "total", "top",
                                    "menu", "seat", "photo", "commitment", "map", "coupon", "reserve"])
    df.columns = ['日にち', "曜日", "合計", '店舗トップ', 'メニュー',
                  '席・個室・貸切', '写真', 'こだわり', '地図', 'クーポン', '予約']

    basepath, ext = os.path.splitext(os.path.basename(__file__))
    oldpath = 'data_wana_gn_sp_{}.csv'.format(fes_query)

    response = HttpResponse(content_type='text/csv; charset=UTF-8-sig')
    response['Content-Disposition'] = 'attachment; filename={}'.format(oldpath)
    df.to_csv(path_or_buf=response, index=False, float_format='%.2f', decimal=",")

    return response


def wana_hp_sp_get(request):
    fes_query = request.GET.get('q')

    # month_keyでクエリセット
    qs = models.Wana_hp_sp_scrape.objects.filter(month_key=fes_query)
    print(fes_query)

    df = read_frame(qs, fieldnames=["date", "week", "pv_all_sp", "pv_top_sp", "pv_coupon_sp", "cvr_sp",
                                    "tell_sp", "reserve_sp", "reserve_hp", "reserve_homepage", "day_over_day_changes"])
    df.columns = ["日付", "曜日", "店舗総PV（SP）", "店舗TOP PV（SP）", "クーポンページPV（SP）",
                  "CVR（SP）", "電話件数（SP）", "予約件数（SP）", "予約件数（ホットペッパー）", "予約件数（ホームページ）", "前日比"]

    basepath, ext = os.path.splitext(os.path.basename(__file__))
    oldpath = 'data_wana_hp_sp_{}.csv'.format(fes_query)

    response = HttpResponse(content_type='text/csv; charset=UTF-8-sig')
    response['Content-Disposition'] = 'attachment; filename={}'.format(oldpath)
    df.to_csv(path_or_buf=response, index=False, float_format='%.2f', decimal=",")

    return response


def wana_tb_sp_get(request):
    fes_query = request.GET.get('q')

    # month_keyでクエリセット
    qs = models.Wana_tb_sp_scrape.objects.filter(month_key=fes_query)
    print(fes_query)

    df = read_frame(qs, fieldnames=["date", "week", "top", "photo", "photo_info",
                                    "rating", "menu", "map", "coupon", "p_coupon", "seat", "other", "total"])
    df.columns = ["日付", "曜日", "店舗トップ", "写真一覧", "写真詳細", "口コミ・評価",
                  "メニュー", "お店地図", "クーポン", "プレミアムクーポン", "座席情報", "その他", "店舗全体（合計）"]

    basepath, ext = os.path.splitext(os.path.basename(__file__))
    oldpath = 'data_wana_tb_sp_{}.csv'.format(fes_query)

    response = HttpResponse(content_type='text/csv; charset=UTF-8-sig')
    response['Content-Disposition'] = 'attachment; filename={}'.format(oldpath)
    df.to_csv(path_or_buf=response, index=False, float_format='%.2f', decimal=",")

    return response


def toro(request):
    return render(request, "scr/toro.html")
# class Garage(TemplateView):
#     template_name = "scr/garage.html"


def toro_gn_sp_get(request):
    fes_query = request.GET.get('q')

    # month_keyでクエリセット
    qs = models.Toro_gn_sp_scrape.objects.filter(month_key=fes_query)
    print(fes_query)

    df = read_frame(qs, fieldnames=["date", "week", "total", "top",
                                    "menu", "seat", "photo", "commitment", "map", "coupon", "reserve"])
    df.columns = ['日にち', "曜日", "合計", '店舗トップ', 'メニュー',
                  '席・個室・貸切', '写真', 'こだわり', '地図', 'クーポン', '予約']

    basepath, ext = os.path.splitext(os.path.basename(__file__))
    oldpath = 'data_toro_gn_sp_{}.csv'.format(fes_query)

    response = HttpResponse(content_type='text/csv; charset=UTF-8-sig')
    response['Content-Disposition'] = 'attachment; filename={}'.format(oldpath)
    df.to_csv(path_or_buf=response, index=False, float_format='%.2f', decimal=",")

    return response


def toro_hp_sp_get(request):
    fes_query = request.GET.get('q')

    # month_keyでクエリセット
    qs = models.Toro_hp_sp_scrape.objects.filter(month_key=fes_query)
    print(fes_query)

    df = read_frame(qs, fieldnames=["date", "week", "pv_all_sp", "pv_top_sp", "pv_coupon_sp", "cvr_sp",
                                    "tell_sp", "reserve_sp", "reserve_hp", "reserve_homepage", "day_over_day_changes"])
    df.columns = ["日付", "曜日", "店舗総PV（SP）", "店舗TOP PV（SP）", "クーポンページPV（SP）",
                  "CVR（SP）", "電話件数（SP）", "予約件数（SP）", "予約件数（ホットペッパー）", "予約件数（ホームページ）", "前日比"]

    basepath, ext = os.path.splitext(os.path.basename(__file__))
    oldpath = 'data_toro_hp_sp_{}.csv'.format(fes_query)

    response = HttpResponse(content_type='text/csv; charset=UTF-8-sig')
    response['Content-Disposition'] = 'attachment; filename={}'.format(oldpath)
    df.to_csv(path_or_buf=response, index=False, float_format='%.2f', decimal=",")

    return response


def toro_tb_sp_get(request):
    fes_query = request.GET.get('q')

    # month_keyでクエリセット
    qs = models.Toro_tb_sp_scrape.objects.filter(month_key=fes_query)
    print(fes_query)

    df = read_frame(qs, fieldnames=["date", "week", "top", "photo", "photo_info",
                                    "rating", "menu", "map", "coupon", "p_coupon", "seat", "other", "total"])
    df.columns = ["日付", "曜日", "店舗トップ", "写真一覧", "写真詳細", "口コミ・評価",
                  "メニュー", "お店地図", "クーポン", "プレミアムクーポン", "座席情報", "その他", "店舗全体（合計）"]

    basepath, ext = os.path.splitext(os.path.basename(__file__))
    oldpath = 'data_toro_tb_sp_{}.csv'.format(fes_query)

    response = HttpResponse(content_type='text/csv; charset=UTF-8-sig')
    response['Content-Disposition'] = 'attachment; filename={}'.format(oldpath)
    df.to_csv(path_or_buf=response, index=False, float_format='%.2f', decimal=",")

    return response
