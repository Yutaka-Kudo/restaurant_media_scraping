from dateutil.relativedelta import relativedelta
from django.shortcuts import render, redirect

from django_pandas.io import read_frame
from numpy import select
import pandas as pd
import os
from django.http import HttpResponse
from scraping import models
from devtools import debug
import datetime


def admin_scr(request):
    return redirect('/admin/')


def dev(request):
    return render(request, 'scr/dev.html')


def index(request):
    return render(request, "scr/index.html")


def store_page(request, store):
    global span_list
    if store == "fes":
        dbmodel = models.Fes_gn_sp_scrape
    elif store == "garage":
        dbmodel = models.Grg_gn_sp_scrape
    elif store == "tourou":
        dbmodel = models.Toro_gn_sp_scrape
    elif store == "wanaichi":
        dbmodel = models.Wana_gn_sp_scrape
    elif store == "wananakame":
        dbmodel = models.Wananakame_gn_sp_scrape
    obj = dbmodel.objects.all().order_by("date")
    span_list = []
    for i in obj:
        span_list.append(i.month_key)
    span_list = sorted(set(span_list), reverse=True)
    return render(request, "scr/store.html", {"store": store, "span_list": span_list})


def select_dbmodel(store: str, media: str):
    if media == "gn":
        fieldnames = ["date", "week", "total", "top", "menu", "seat", "photo", "commitment", "map", "coupon", "reserve"]
        rename_col = ['日付', "曜日", "合計", '店舗トップ', 'メニュー', '席・個室・貸切', '写真', 'こだわり', '地図', 'クーポン', '予約']
        if store == "fes":
            dbmodel = models.Fes_gn_sp_scrape
        elif store == "garage":
            dbmodel = models.Grg_gn_sp_scrape
        elif store == "tourou":
            dbmodel = models.Toro_gn_sp_scrape
        elif store == "wanaichi":
            dbmodel = models.Wana_gn_sp_scrape
        elif store == "wananakame":
            dbmodel = models.Wananakame_gn_sp_scrape
    elif media == "hp":
        fieldnames = ["date", "week", "pv_all_sp", "pv_top_sp", "pv_coupon_sp", "cvr_sp", "tell_sp", "reserve_sp", "reserve_hp", "reserve_homepage", "day_over_day_changes"]
        rename_col = ["日付", "曜日", "店舗総PV（SP）", "店舗TOP PV（SP）", "クーポンページPV（SP）", "CVR（SP）", "電話件数（SP）", "予約件数（SP）", "予約件数（ホットペッパー）", "予約件数（ホームページ）", "前日比"]
        if store == "fes":
            dbmodel = models.Fes_hp_sp_scrape
        elif store == "garage":
            dbmodel = models.Grg_hp_sp_scrape
        elif store == "tourou":
            dbmodel = models.Toro_hp_sp_scrape
        elif store == "wanaichi":
            dbmodel = models.Wana_hp_sp_scrape
        elif store == "wananakame":
            dbmodel = models.Wananakame_hp_sp_scrape
    elif media == "tb":
        fieldnames = ["date", "week", "top", "photo", "photo_info", "rating", "menu", "map", "coupon", "p_coupon", "seat", "other", "total"]
        rename_col = ["日付", "曜日", "店舗トップ", "写真一覧", "写真詳細", "口コミ・評価", "メニュー", "お店地図", "クーポン", "プレミアムクーポン", "座席情報", "その他", "店舗全体（合計）"]
        if store == "fes":
            dbmodel = models.Fes_tb_sp_scrape
        elif store == "garage":
            dbmodel = models.Grg_tb_sp_scrape
        elif store == "tourou":
            dbmodel = models.Toro_tb_sp_scrape
        elif store == "wanaichi":
            dbmodel = models.Wana_tb_sp_scrape
        elif store == "wananakame":
            dbmodel = models.Wananakame_tb_sp_scrape
    return dbmodel, fieldnames, rename_col


def create_df(y_m: str, store: str, media: str, interval: str, start="", end=""):
    dbmodel, fieldnames, rename_col = select_dbmodel(store, media)

    if interval == "daily":
        # month_keyでクエリセット
        qs = dbmodel.objects.filter(month_key=y_m).order_by('date')
        print(y_m)
    elif interval == "weekly":
        # if move == "before":
        #     to_day: datetime.date = trans_date(y_m) - relativedelta(days=7)
        # elif move == "after":
        #     to_day: datetime.date = trans_date(y_m) + relativedelta(days=7)
        #     if to_day > dbmodel.objects.latest('date').date:
        #         to_day = dbmodel.objects.latest('date').date
        # else:
        #     to_day: datetime.date = dbmodel.objects.latest('date').date
        # before6: datetime.date = to_day - relativedelta(days=6)
        # qs = dbmodel.objects.filter(date__lte=to_day, date__gte=before6).order_by('-date')
        # for i in qs:
        #     if i.week == "土":  # 土曜を探して起点にする
        #         to_day = i.date
        #         break
        # before12weeks: datetime.date = to_day - relativedelta(days=83)
        # dateでクエリセット
        qs = dbmodel.objects.filter(date__lte=start, date__gte=end).order_by('date')

    df = read_frame(qs, fieldnames=fieldnames)
    df.columns = rename_col

    return df


def trans_monthkey(i):
    if type(i) == str:
        result = datetime.datetime.strptime(i, '%Y-%m').date()
    elif type(i) == datetime.date:
        result = datetime.date.strftime(i, '%Y-%m')
    return result


def trans_date(i):  # 0000-00-00の形
    if type(i) == str:
        result = datetime.datetime.strptime(i, '%Y-%m-%d').date()
    elif type(i) == datetime.date:
        result = datetime.date.strftime(i, '%Y-%m-%d')
    return result


def download_excel(request, store: str, media: str):
    y_m: str = request.GET.get('q')
    df = create_df(y_m, store, media, interval="daily")

    basepath, ext = os.path.splitext(os.path.basename(__file__))
    oldpath = f'data_{store}_gn_sp_{y_m}.csv'

    response = HttpResponse(content_type='text/csv; charset=UTF-8-sig')
    response['Content-Disposition'] = 'attachment; filename={}'.format(oldpath)
    df.to_csv(path_or_buf=response, index=False, float_format='%.2f', decimal=",")

    return response


def chart(request, store: str, media: str):
    y_m: str = request.GET.get('q')

    # beforeボタン、afterボタン押下時
    move = request.GET.get('move')
    if move == "before":
        date = trans_monthkey(y_m)
        date -= relativedelta(months=1)
        y_m = trans_monthkey(date)
    elif move == "after":
        date = trans_monthkey(y_m)
        date += relativedelta(months=1)
        y_m = trans_monthkey(date)
    else:
        pass
    df = create_df(y_m, store, media, interval="daily")

    dates = [datetime.date.strftime(s, '%Y-%m-%d') for s in df["日付"]]
    xticks = list(dates + df["曜日"])

    if media == "gn":
        total = list(df["合計"])
        data2 = list(df["店舗トップ"])
        data2_name = "店舗トップ"
        data3 = list(df["地図"])
        data3_name = "地図"
        data4 = list(df["クーポン"])
        data4_name = "クーポン"
        data5 = list(df["予約"])
        data5_name = "予約"

        total_1 = df["合計"].sum()
        total_2 = df["店舗トップ"].sum()
        total_3 = df["地図"].sum()
        total_4 = df["クーポン"].sum()
        total_5 = df["予約"].sum()
    if media == "hp":
        total = list(df["店舗総PV（SP）"])
        data2 = list(df["店舗TOP PV（SP）"])
        data2_name = "店舗TOP PV（SP）"
        # = list(df["クーポンページPV（SP）"])
        # = list(df["クーポンページPV（SP）"])
        data3 = list(df["CVR（SP）"])
        data3 = [float(i[:-1]) if i != "-" else 0 for i in list(df["CVR（SP）"])]
        data3_name = "CVR（SP）"
        data4 = list(df["予約件数（SP）"])
        data4_name = "予約件数（SP）"
        data5 = list(df["予約件数（ホットペッパー）"])
        data5_name = "予約件数（ホットペッパー）"
        #  = list(df["予約件数（ホームページ）"])
        #  = list(df["予約件数（ホームページ）"])
        total_1 = df["店舗総PV（SP）"].sum()
        total_2 = df["店舗TOP PV（SP）"].sum()
        total_3 = str(round(sum(data3) / len(data3), 1)) + "%"
        total_4 = df["予約件数（SP）"].sum()
        total_5 = df["予約件数（ホットペッパー）"].sum()
    if media == "tb":
        total = list(df["店舗全体（合計）"])
        data2 = list(df["店舗トップ"])
        data2_name = "店舗トップ"
        data3 = list(df["口コミ・評価"])
        data3_name = "口コミ・評価"
        data4 = list(df["お店地図"])
        data4_name = "お店地図"
        data5 = list(df["クーポン"])
        data5_name = "クーポン"
        total_1 = df["店舗全体（合計）"].sum()
        total_2 = df["店舗トップ"].sum()
        total_3 = df["口コミ・評価"].sum()
        total_4 = df["お店地図"].sum()
        total_5 = df["クーポン"].sum()

    context = {
        "date": y_m,
        "store": store,
        "media": media,
        "df": df,
        "xticks": xticks,
        "total": total,
        "data2": data2,
        "data2_name": data2_name,
        "data3": data3,
        "data3_name": data3_name,
        "data4": data4,
        "data4_name": data4_name,
        "data5": data5,
        "data5_name": data5_name,
        "total_1": total_1,
        "total_2": total_2,
        "total_3": total_3,
        "total_4": total_4,
        "total_5": total_5,
    }
    return render(request, "scr/chart.html", context)


def chart_weekly(request, store: str, media: str):
    dbmodel, _, _ = select_dbmodel(store, media)
    y_m_d: str = request.GET.get('q')
    if not y_m_d:  # requestgetがなかったら＝初期動作
        to_day: datetime.date = dbmodel.objects.latest('date').date
        before6: datetime.date = to_day - relativedelta(days=6)
        qs = dbmodel.objects.filter(date__lte=to_day, date__gte=before6).order_by('-date')
        for i in qs:
            if i.week == "土":  # 土曜を探して起点にする
                to_day = i.date
                break
        # y_m_d = str(to_day)

    # beforeボタン、afterボタン押下時
    move = request.GET.get('move')
    if move == "before":
        to_day: datetime.date = trans_date(y_m_d) - relativedelta(days=7)
    elif move == "after":
        to_day: datetime.date = trans_date(y_m_d) + relativedelta(days=7)
        if to_day > dbmodel.objects.latest('date').date:
            to_day = trans_date(y_m_d)

    before12weeks: datetime.date = to_day - relativedelta(days=83)

    _df = create_df(None, store, media, interval="weekly", start=to_day, end=before12weeks)
    list = []
    # 7日ごとの合計をリストに挿入
    for i in range(0, len(_df), 7):
        list.append(_df[i:i+7].sum())

    df = pd.DataFrame(list)
    dates = [trans_date(s)+"_"+trans_date(s+relativedelta(days=6)) for s in _df["日付"][::7]]
    xticks = dates

    if media == "gn":
        total = df["合計"].values.tolist()
        data2 = df["店舗トップ"].values.tolist()
        data2_name = "店舗トップ"
        data3 = df["地図"].values.tolist()
        data3_name = "地図"
        data4 = df["クーポン"].values.tolist()
        data4_name = "クーポン"
        data5 = df["予約"].values.tolist()
        data5_name = "予約"

        total_1 = df["合計"].sum()
        total_2 = df["店舗トップ"].sum()
        total_3 = df["地図"].sum()
        total_4 = df["クーポン"].sum()
        total_5 = df["予約"].sum()
    if media == "hp":
        total = df["店舗総PV（SP）"].values.tolist()
        data2 = df["店舗TOP PV（SP）"].values.tolist()
        data2_name = "店舗TOP PV（SP）"
        # = df["クーポンページPV（SP）"].values.tolist()
        # = df["クーポンページPV（SP）"].values.tolist()
        cvr_list = [float(i[:-1]) if i != "-" else 0 for i in _df["CVR（SP）"].values.tolist()]
        cvr_result = []
        for i in range(0, len(_df), 7):
            cvr_result.append(round(sum(cvr_list[i:i+7]) / len(cvr_list[i:i+7]),1))
        data3 = cvr_result
        data3_name = "CVR（SP）"
        data4 = df["予約件数（SP）"].values.tolist()
        data4_name = "予約件数（SP）"
        data5 = df["予約件数（ホットペッパー）"].values.tolist()
        data5_name = "予約件数（ホットペッパー）"
        #  = df["予約件数（ホームページ）"].values.tolist()
        #  = df["予約件数（ホームページ）"].values.tolist()
        total_1 = df["店舗総PV（SP）"].sum()
        total_2 = df["店舗TOP PV（SP）"].sum()
        total_3 = str(round(sum(data3) / len(data3), 1)) + "%"
        total_4 = df["予約件数（SP）"].sum()
        total_5 = df["予約件数（ホットペッパー）"].sum()
    if media == "tb":
        total = df["店舗全体（合計）"].values.tolist()
        data2 = df["店舗トップ"].values.tolist()
        data2_name = "店舗トップ"
        data3 = df["口コミ・評価"].values.tolist()
        data3_name = "口コミ・評価"
        data4 = df["お店地図"].values.tolist()
        data4_name = "お店地図"
        data5 = df["クーポン"].values.tolist()
        data5_name = "クーポン"
        total_1 = df["店舗全体（合計）"].sum()
        total_2 = df["店舗トップ"].sum()
        total_3 = df["口コミ・評価"].sum()
        total_4 = df["お店地図"].sum()
        total_5 = df["クーポン"].sum()

    context = {
        "date": str(to_day),
        "span_list": span_list,
        "store": store,
        "media": media,
        "df": df,
        "xticks": xticks,
        "total": total,
        "data2": data2,
        "data2_name": data2_name,
        "data3": data3,
        "data3_name": data3_name,
        "data4": data4,
        "data4_name": data4_name,
        "data5": data5,
        "data5_name": data5_name,
        "total_1": total_1,
        "total_2": total_2,
        "total_3": total_3,
        "total_4": total_4,
        "total_5": total_5,
    }
    return render(request, "scr/chart_weekly.html", context)


def chart_GMB(request, store):
    if store == "fes":
        dbmodel = models.Fes_GMB
    elif store == "garage":
        dbmodel = models.Grg_GMB
    elif store == "tourou":
        dbmodel = models.Toro_GMB
    elif store == "wanaichi":
        dbmodel = models.Wanaichi_GMB
    elif store == "wananakame":
        dbmodel = models.Wananakame_GMB

    df = pd.DataFrame(dbmodel.objects.all().order_by('span_id').values())

    xticks = list(df["span"])

    total = list(df["total_show"])
    data2 = list(df["total_search"])
    data2_name = "合計検索数"
    data3 = list(df["direct_search"])
    data3_name = "直接検索数"
    data4 = list(df["indirect_search"])
    data4_name = "間接検索数"
    data5 = list(df["total_action"])
    data5_name = "合計反応数"

    context = {
        "store": store,
        "df": df,
        "xticks": xticks,
        "total": total,
        "data2": data2,
        "data2_name": data2_name,
        "data3": data3,
        "data3_name": data3_name,
        "data4": data4,
        "data4_name": data4_name,
        "data5": data5,
        "data5_name": data5_name,
    }
    return render(request, "scr/chart_GMB.html", context)
