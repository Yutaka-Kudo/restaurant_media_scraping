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
    span_list_fes = []
    obj = models.Fes_gn_scrape.objects.all().order_by("date")
    for i in obj:
        span_list_fes.append(i.month_key)
    span_list_fes = sorted(set(span_list_fes), reverse=True)

    span_list_garage = []
    obj = models.Grg_gn_scrape.objects.all().order_by("date")
    for i in obj:
        span_list_garage.append(i.month_key)
    span_list_garage = sorted(set(span_list_garage), reverse=True)

    span_list_tourou = []
    obj = models.Toro_gn_scrape.objects.all().order_by("date")
    for i in obj:
        span_list_tourou.append(i.month_key)
    span_list_tourou = sorted(set(span_list_tourou), reverse=True)

    span_list_wanaichi = []
    obj = models.Wana_gn_scrape.objects.all().order_by("date")
    for i in obj:
        span_list_wanaichi.append(i.month_key)
    span_list_wanaichi = sorted(set(span_list_wanaichi), reverse=True)

    span_list_wananakame = []
    obj = models.Wananakame_gn_scrape.objects.all().order_by("date")
    for i in obj:
        span_list_wananakame.append(i.month_key)
    span_list_wananakame = sorted(set(span_list_wananakame), reverse=True)
    span_list_wananakame_tb = []
    obj = models.Wananakame_tb_scrape.objects.all().order_by("date")
    for i in obj:
        span_list_wananakame_tb.append(i.month_key)
    span_list_wananakame_tb = sorted(set(span_list_wananakame_tb), reverse=True)

    context = {
        # "store": store,
        #  "span_list": span_list,
        "span_list_fes": span_list_fes,
        "span_list_garage": span_list_garage,
        "span_list_tourou": span_list_tourou,
        "span_list_wanaichi": span_list_wanaichi,
        "span_list_wananakame": span_list_wananakame,
        "span_list_wananakame_tb": span_list_wananakame_tb,
    }
    return render(request, "scr/index.html", context)


def select_dbmodel(store: str, media: str):
    if media == "gn":
        fieldnames = ['date', 'week', 'total_pv_sp', 'top_pv_sp', 'menu_pv_sp', 'seat_pv_sp', 'photo_pv_sp', 'commitment_pv_sp', 'map_pv_sp', 'coupon_pv_sp', 'reserve_pv_sp', 'total_pv_pc', 'top_pv_pc', 'menu_pv_pc', 'seat_pv_pc', 'photo_pv_pc', 'commitment_pv_pc', 'map_pv_pc', 'coupon_pv_pc', 'reserve_pv_pc', 'total_pv_app',
                      'top_pv_app', 'menu_pv_app', 'seat_pv_app', 'photo_pv_app', 'commitment_pv_app', 'map_pv_app', 'coupon_pv_app', 'reserve_pv_app', 'reserve_course_number', 'reserve_course_people', 'reserve_course_price', 'reserve_seatonly_number', 'reserve_seatonly_people', 'reserve_request_number', 'reserve_request_people', 'reserve_total']
        rename_col = ['日付', "曜日", "合計PV_SP", "店舗トップPV_SP", "メニューPV_SP", "席個室貸切PV_SP", "写真PV_SP", "こだわりPV_SP", "地図PV_SP", "クーポンPV_SP", "予約PV_SP", "合計PV_PC", "店舗トップPV_PC", "メニューPV_PC", "席個室貸切PV_PC", "写真PV_PC", "こだわりPV_PC", "地図PV_PC", "クーポンPV_PC",
                      "予約PV_PC", "合計PV_app", "店舗トップPV_app", "メニューPV_app", "席個室貸切PV_app", "写真PV_app", "こだわりPV_app", "地図PV_app", "クーポンPV_app", "予約PV_app", "予約_コース_件数", "予約_コース_人数", "予約_コース_金額", "予約_席のみ_件数", "予約_席のみ_人数", "予約_リクエスト_件数", "予約_リクエスト_人数", "予約_合計件数"]
        if store == "fes":
            dbmodel = models.Fes_gn_scrape
        elif store == "garage":
            dbmodel = models.Grg_gn_scrape
        elif store == "tourou":
            dbmodel = models.Toro_gn_scrape
        elif store == "wanaichi":
            dbmodel = models.Wana_gn_scrape
        elif store == "wananakame":
            dbmodel = models.Wananakame_gn_scrape
    elif media == "hp":
        fieldnames = ["date", "week", "pv_all_sp", "pv_top_sp", "pv_coupon_sp", "cvr_sp", "tell_sp", "reserve_sp", "reserve_hp_sp",
                      "reserve_homepage_sp", "pv_all_pc", "pv_top_pc", "pv_coupon_pc", "cvr_pc", "tell_pc", "reserve_pc", "reserve_hp_pc", "reserve_homepage_pc"]
        rename_col = ["日付", "曜日", "店舗総PV_sp", "店舗TOP PV_sp", "クーポンページPV_sp", "CVR_sp", "電話件数_sp", "予約件数_sp", "予約件数_ホットペッパー_sp",
                      "予約件数_ホームページ_sp", "店舗総PV_pc", "店舗TOP PV_pc", "クーポンページPV_pc", "CVR_pc", "電話件数_pc", "予約件数_pc", "予約件数_ホットペッパー_pc", "予約件数_ホームページ_pc"]
        if store == "fes":
            dbmodel = models.Fes_hp_scrape
        elif store == "garage":
            dbmodel = models.Grg_hp_scrape
        elif store == "tourou":
            dbmodel = models.Toro_hp_scrape
        elif store == "wanaichi":
            dbmodel = models.Wana_hp_scrape
        elif store == "wananakame":
            dbmodel = models.Wananakame_hp_scrape
    elif media == "tb":
        fieldnames = ["date", "week", "top_pv_sp", "photo_pv_sp", "photo_info_pv_sp", "rating_pv_sp", "menu_pv_sp", "map_pv_sp", "coupon_pv_sp", "p_coupon_pv_sp", "seat_pv_sp", "other_pv_sp", "total_pv_sp", "top_pv_pc",
                      "photo_food_pv_pc", "photo_drink_pv_pc", "photo_interior_pv_pc", "photo_exterior_pv_pc", "rating_pv_pc", "menu_pv_pc", "map_coupon_pv_pc", "p_coupon_pv_pc", "seat_pv_pc", "other_pv_pc", "total_pv_pc", "net_reserve"]
        rename_col = ["日付", "曜日", "店舗トップPV_sp", "写真一覧PV_sp", "写真詳細PV_sp", "口コミPV_sp", "メニューPV_sp", "地図PV_sp", "クーポンPV_sp", "プレミアムクーポンPV_sp", "座席情報PV_sp", "その他PV_sp", "合計PV_sp",
                      "店舗トップPV_pc", "料理写真PV_pc", "ドリンク写真_pc", "内観写真_pc", "外観写真_pc", "口コミPV_pc", "メニューPV_pc", "地図_クーポンPV_pc", "プレミアムクーポンPV_pc", "座席情報PV_pc", "その他PV_pc", "合計PV_pc", "ネット予約"]
        if store == "fes":
            dbmodel = models.Fes_tb_scrape
        elif store == "garage":
            dbmodel = models.Grg_tb_scrape
        elif store == "tourou":
            dbmodel = models.Toro_tb_scrape
        elif store == "wanaichi":
            dbmodel = models.Wana_tb_scrape
        elif store == "wananakame":
            dbmodel = models.Wananakame_tb_scrape
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
    oldpath = f'data_{store}_gn_{y_m}.csv'

    response = HttpResponse(content_type='text/csv; charset=UTF-8-sig')
    response['Content-Disposition'] = 'attachment; filename={}'.format(oldpath)
    df.to_csv(path_or_buf=response, index=False, float_format='%.2f', decimal=",")

    return response


def chart(request, store: str, media: str):
    daily_flg = request.GET.get('daily_flg')
    if daily_flg:
        y_m: str = request.GET.get('q')
        if not y_m:
            y_m: str = request.GET.get('date')


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


    else:
        dbmodel, _, _ = select_dbmodel(store, media)
        y_m_d: str = request.GET.get('q')
        current_date = request.GET.get('date')
        if not y_m_d and not current_date:  # requestgetがなかったら＝初期動作
            to_day: datetime.date = dbmodel.objects.latest('date').date
            before6: datetime.date = to_day - relativedelta(days=6)
            qs = dbmodel.objects.filter(date__lte=to_day, date__gte=before6).order_by('-date')
            for i in qs:
                if i.week == "土":  # 土曜を探して起点にする
                    to_day = i.date
                    break

        # beforeボタン、afterボタン押下時
        move = request.GET.get('move')
        if move == "before":
            to_day: datetime.date = trans_date(y_m_d) - relativedelta(days=7)
        elif move == "after":
            to_day: datetime.date = trans_date(y_m_d) + relativedelta(days=7)
            if to_day > dbmodel.objects.latest('date').date: # 未来にはいけないよ
                to_day = trans_date(y_m_d)
        
        if current_date:
            to_day = trans_date(current_date)

        before12weeks: datetime.date = to_day - relativedelta(days=83)

        _df = create_df(None, store, media, interval="weekly", start=to_day, end=before12weeks)
        data_list = []
        # 7日ごとの合計をリストに挿入
        for i in range(0, len(_df), 7):
            data_list.append(_df[i:i+7].sum())

        df = pd.DataFrame(data_list)
        dates = [trans_date(s)+"_"+trans_date(s+relativedelta(days=6))[5:] for s in _df["日付"][::7]]
        xticks = dates


    data10, data11, data12, data13, data14, data15, data16, data17, data18, data19, data20, data21, data22, data10_name, data11_name, data12_name, data13_name, data14_name, data15_name, data16_name, data17_name, data18_name, data19_name, data20_name, data21_name, data22_name, total_10, total_11, total_12, total_13, total_14, total_15, total_16, total_17, total_18, total_19, total_20, total_21, total_22 = None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None


    if media == "gn":
        total = list(df["合計PV_SP"]+df["合計PV_PC"]+df["合計PV_app"])
        total_1 = sum(total)
        data2 = list(df["合計PV_SP"])
        data2_name = "合計PV_スマホ"
        total_2 = sum(data2)
        data3 = list(df["合計PV_PC"])
        data3_name = "合計PV_PC"
        total_3 = sum(data3)
        data4 = list(df["合計PV_app"])
        data4_name = "合計PV_app"
        total_4 = sum(data4)
        data5 = list(df["店舗トップPV_SP"]+df["店舗トップPV_PC"]+df["店舗トップPV_app"])
        data5_name = "店舗トップPV_合計"
        total_5 = sum(data5)
        data6 = list(df["店舗トップPV_SP"])
        data6_name = "店舗トップPV_スマホ"
        total_6 = sum(data6)
        data7 = list(df["店舗トップPV_PC"])
        data7_name = "店舗トップPV_PC"
        total_7 = sum(data7)
        data8 = list(df["店舗トップPV_app"])
        data8_name = "店舗トップPV_app"
        total_8 = sum(data8)
        # data9 = list(df["地図PV_SP"]+df["地図PV_PC"]+df["地図PV_app"])
        data9 = [round((i / i2)*100,3) for i, i2 in zip(list(df["地図PV_SP"]+df["地図PV_PC"]+df["地図PV_app"]), data5)]
        # data9_name = "地図PV_合計"
        data9_name = "地図PV率"
        # total_9 = sum(data9)
        total_9 = str(round(sum(list(df["地図PV_SP"]+df["地図PV_PC"]+df["地図PV_app"])) / total_5 * 100, 1))+"%"
        data10 = list(df["地図PV_SP"])
        data10_name = "地図PV_スマホ"
        total_10 = sum(data10)
        data11 = list(df["地図PV_PC"])
        data11_name = "地図PV_PC"
        total_11 = sum(data11)
        data12 = list(df["地図PV_app"])
        data12_name = "地図PV_app"
        total_12 = sum(data12)
        # data13 = list(df["クーポンPV_SP"]+df["クーポンPV_PC"]+df["クーポンPV_app"])
        data13 = [round((i / i2)*100, 3) for i, i2 in zip(list(df["クーポンPV_SP"]+df["クーポンPV_PC"]+df["クーポンPV_app"]), data5)]
        # data13_name = "クーポンPV_合計"
        data13_name = "クーポンPV率"
        # total_13 = sum(data13)
        total_13 = str(round(sum(list(df["クーポンPV_SP"]+df["クーポンPV_PC"]+df["クーポンPV_app"])) / total_5 * 100, 1))+"%"
        data14 = list(df["クーポンPV_SP"])
        data14_name = "クーポンPV_スマホ"
        total_14 = sum(data14)
        data15 = list(df["クーポンPV_PC"])
        data15_name = "クーポンPV_PC"
        total_15 = sum(data15)
        data16 = list(df["クーポンPV_app"])
        data16_name = "クーポンPV_app"
        total_16 = sum(data16)
        # data17 = list(df["予約PV_SP"]+df["予約PV_PC"]+df["予約PV_app"])
        data17 = [round((i / i2)*100, 3) for i, i2 in zip(list(df["予約PV_SP"]+df["予約PV_PC"]+df["予約PV_app"]), data5)]
        # data17_name = "予約PV_合計"
        data17_name = "予約PV率_合計"
        # total_17 = sum(data17)
        total_17 = str(round(sum(list(df["予約PV_SP"]+df["予約PV_PC"]+df["予約PV_app"])) / total_5 * 100, 1))+"%"
        # data18 = list(df["予約PV_SP"])
        data18 = []
        for i, i2 in zip(list(df["予約PV_SP"]), data6):
            if i2 == 0:
                data18.append(0)
            else:
                data18.append(round((i / i2)*100, 3))      
        # data18_name = "予約PV率_スマホ"
        data18_name = "予約PV率_スマホ"
        # total_18 = sum(data18)
        total_18 = str(round(sum(list(df["予約PV_SP"])) / total_6 * 100, 1))+"%"
        # data19 = list(df["予約PV_PC"])
        data19 = [round((i / i2)*100, 3) for i, i2 in zip(list(df["予約PV_PC"]), data7)]
        # data19_name = "予約PV率_PC"
        data19_name = "予約PV率_PC"
        # total_19 = sum(data19)
        total_19 = str(round(sum(list(df["予約PV_PC"])) / total_7 * 100, 1))+"%"
        # data20 = list(df["予約PV_app"])
        data20 = []
        for i, i2 in zip(list(df["予約PV_app"]), data8):
            if i2 == 0:
                data20.append(0)
            else:
                data20.append(round((i / i2)*100, 3))
        # data20_name = "予約PV率_app"
        data20_name = "予約PV率_app"
        # total_20 = sum(data20)
        total_20 = str(round(sum(list(df["予約PV_app"])) / total_8 * 100, 1))+"%"
        data21 = list(df["予約_合計件数"])
        data21_name = "ネット予約_合計件数"
        total_21 = sum(data21)
        data22 = [round((i / i2)*100, 1) for i, i2 in zip(data21, data5)]
        data22_name = "CV率 ネット予約/TOP "
        total_22 = str(round(total_21 / total_5 * 100, 1))+"%"

    if media == "hp":
        total = list(df["店舗総PV_sp"]+df["店舗総PV_pc"])
        total_1 = sum(total)
        data2 = list(df["店舗総PV_sp"])
        data2_name = "店舗総PV_スマホ"
        total_2 = sum(data2)
        data3 = list(df["店舗総PV_pc"])
        data3_name = "店舗総PV_pc"
        total_3 = sum(data3)
        data4 = list(df["店舗TOP PV_sp"]+df["店舗TOP PV_pc"])
        data4_name = "店舗TOPpv合計"
        total_4 = sum(data4)
        data5 = list(df["店舗TOP PV_sp"])
        data5_name = "店舗TOP PV_スマホ"
        total_5 = sum(data5)
        data6 = list(df["店舗TOP PV_pc"])
        data6_name = "店舗TOP PV_pc"
        total_6 = sum(data6)
        data7 = list(df["クーポンページPV_sp"]+df["クーポンページPV_pc"])
        data7_name = "クーポンページPV合計"
        total_7 = sum(data7)
        data8 = list(df["クーポンページPV_sp"])
        data8_name = "クーポンページPV_スマホ"
        total_8 = sum(data8)
        data9 = list(df["クーポンページPV_pc"])
        data9_name = "クーポンページPV_pc"
        total_9 = sum(data9)
        data10 = list(df["電話件数_sp"]+df["電話件数_pc"])
        data10_name = "電話_合計"
        total_10 = sum(data10)
        data11 = list(df["電話件数_sp"])
        data11_name = "電話_スマホ"
        total_11 = sum(data11)
        data12 = list(df["電話件数_pc"])
        data12_name = "電話_pc"
        total_12 = sum(data12)
        data13 = list(df["予約件数_sp"]+df["予約件数_pc"])
        data13_name = "ネット予約_合計"
        total_13 = sum(data13)
        data14 = list(df["予約件数_sp"])
        data14_name = "ネット予約_スマホ"
        total_14 = sum(data14)
        data15 = list(df["予約件数_pc"])
        data15_name = "ネット予約_pc"
        total_15 = sum(data15)
        data16 = [round((i / i2)*100, 1) for i, i2 in zip(data13, data4)]
        data16_name = "CV率 ネット予約/TOP "
        total_16 = str(round(total_13 / total_4*100, 1))+"%"
        print(data16)

        # total_4 = sum(data4)
        # data5 = [round((x / y)*100, 1) for x, y in zip(data4, data2)]
        # data3 = list(df["CVR（SP）"])
        # data3 = [float(i[:-1]) if i != "-" else 0 for i in list(df["CVR（SP）"])]
        # data3_name = "CVR（SP）"

        # total_1 = sum( data )
        # total_2 = sum( data )
        # total_3 = sum( data )
        # total_4 = sum(data4)
        # total_5 = str(round((total_4 / total_2)*100, 1)) + '%'
    if media == "tb":
        total = list(df["合計PV_sp"]+df["合計PV_pc"])
        total_1 = sum(total)
        data2 = list(df["合計PV_sp"])
        data2_name = "合計PV_スマホ"
        total_2 = sum(data2)
        data3 = list(df["合計PV_pc"])
        data3_name = "合計PV_pc"
        total_3 = sum(data3)
        data4 = list(df["店舗トップPV_sp"]+df["店舗トップPV_pc"])
        data4_name = "店舗トップPV合計"
        total_4 = sum(data4)
        data5 = list(df["店舗トップPV_sp"])
        data5_name = "店舗トップPV_スマホ"
        total_5 = sum(data5)
        data6 = list(df["店舗トップPV_pc"])
        data6_name = "店舗トップPV_pc"
        total_6 = sum(data6)
        data7 = list(df["口コミPV_sp"]+df["口コミPV_pc"])
        data7_name = "口コミPV合計"
        total_7 = sum(data7)
        data8 = list(df["口コミPV_sp"])
        data8_name = "口コミPV_スマホ"
        total_8 = sum(data8)
        data9 = list(df["口コミPV_pc"])
        data9_name = "口コミPV_pc"
        total_9 = sum(data9)
        data10 = list(df["クーポンPV_sp"]+df["地図_クーポンPV_pc"])
        data10_name = "地図・クーポン合計"
        total_10 = sum(data10)
        data11 = list(df["クーポンPV_sp"])
        data11_name = "クーポンPV_スマホ"
        total_11 = sum(data11)
        data12 = list(df["地図_クーポンPV_pc"])
        data12_name = "地図_クーポンPV_pc"
        total_12 = sum(data12)
        data13 = list(df["ネット予約"])
        data13_name = "ネット予約"
        total_13 = sum(data13)
        data14 = [round((i / i2)*100, 1) for i, i2 in zip(data13, data4)]
        data14_name = "CV率 ネット予約/TOP "
        total_14 = str(round(total_13 / total_4*100, 1))+"%"



    context = {
        "store": store,
        "media": media,
        "df": df,
        "xticks": xticks,
        "total": total,
        "data2": data2,
        "data3": data3,
        "data4": data4,
        "data5": data5,
        "data6": data6,
        "data7": data7,
        "data8": data8,
        "data9": data9,
        "data10": data10,
        "data11": data11,
        "data12": data12,
        "data13": data13,
        "data14": data14,
        "data15": data15,
        "data16": data16,
        "data17": data17,
        "data18": data18,
        "data19": data19,
        "data20": data20,
        "data21": data21,
        "data22": data22,
        "data2_name": data2_name,
        "data3_name": data3_name,
        "data4_name": data4_name,
        "data5_name": data5_name,
        "data6_name": data6_name,
        "data7_name": data7_name,
        "data8_name": data8_name,
        "data9_name": data9_name,
        "data10_name": data10_name,
        "data11_name": data11_name,
        "data12_name": data12_name,
        "data13_name": data13_name,
        "data14_name": data14_name,
        "data15_name": data15_name,
        "data16_name": data16_name,
        "data17_name": data17_name,
        "data18_name": data18_name,
        "data19_name": data19_name,
        "data20_name": data20_name,
        "data21_name": data21_name,
        "data22_name": data22_name,
        "total_1": total_1,
        "total_2": total_2,
        "total_3": total_3,
        "total_4": total_4,
        "total_5": total_5,
        "total_6": total_6,
        "total_7": total_7,
        "total_8": total_8,
        "total_9": total_9,
        "total_10": total_10,
        "total_11": total_11,
        "total_12": total_12,
        "total_13": total_13,
        "total_14": total_14,
        "total_15": total_15,
        "total_16": total_16,
        "total_17": total_17,
        "total_18": total_18,
        "total_19": total_19,
        "total_20": total_20,
        "total_21": total_21,
        "total_22": total_22,
    }
    if daily_flg:
        context["date"] = y_m
        if media == "gn":
            return render(request, "scr/chart_gn.html", context)
        elif media == "hp":
            return render(request, "scr/chart_hp.html", context)
        elif media == "tb":
            return render(request, "scr/chart_tb.html", context)
    else:
        context["date"] = str(to_day)
        if media == "gn":
            return render(request, "scr/chart_weekly_gn.html", context)
        elif media == "hp":
            return render(request, "scr/chart_weekly_hp.html", context)
        elif media == "tb":
            return render(request, "scr/chart_weekly_tb.html", context)
        



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
