from dateutil.relativedelta import relativedelta
import pandas as pd
import datetime
from scraping.models import *
from scraping.site_package.my_module import create_dbdict
from django.core.management.base import BaseCommand

from pprint import pprint as pp
import glob

files = glob.glob('scraping/site_package/gmb_csv_data/*.csv')
latest_file = sorted(files, key=lambda file: datetime.datetime.strptime(file[-16:-6].lstrip(' -'), '%Y-%m-%d'))[-1]

# csvファイルの名前の文末の謎数字消す前処理、忘れずに
start_date = datetime.date.strftime(datetime.datetime.strptime(latest_file[-16:-6].lstrip(' -'), '%Y-%m-%d') - relativedelta(days=6), '%Y-%-m-%-d')
# start_date = "2021-4-4"

file_count = 1


def trans_date(i):
    if type(i) == str:
        result = datetime.datetime.strptime(i, '%Y-%m-%d').date()
    elif type(i) == datetime.date:
        result = datetime.date.strftime(i, '%Y-%-m-%-d')
    else:
        result = None
    return result


count = 1
date_list = []
while count <= file_count:
    date_list.append(start_date)
    print(f'append {start_date}')
    start_date = trans_date(start_date)
    start_date += relativedelta(days=7)
    start_date = trans_date(start_date)
    count += 1


class Command(BaseCommand):  # コマンド python manage.py get_insert_db
    def handle(self, *args, **options):
        if input(f'{date_list} OK? y/N: ').lower() == "y":
            for date in date_list:
                end_date = trans_date((trans_date(date) + relativedelta(days=6)))
                for_span = date + "_" + end_date
                for_span_id = "-".join([i.zfill(2) for i in date.split('-')])

                df = pd.read_csv(f'scraping/site_package/GMB insights (Discovery Report) - {date} - {end_date} -.csv', index_col="ビジネス名")

                df = df.drop(df.index[0]).drop(["店舗コード", "住所", "ラベル"], axis=1)

                for index, row in df.iterrows():
                    if "FES" in index:
                        model = Fes_GMB
                    elif "Garage" in index:
                        model = Grg_GMB
                    elif "灯篭" in index:
                        model = Toro_GMB
                    elif "一目" in index:
                        model = Wanaichi_GMB
                    elif "中目黒" in index:
                        model = Wananakame_GMB

                    model.objects.update_or_create(
                        span=for_span,
                        defaults={
                            "span_id": for_span_id,
                            "total_evaluation": row[0],
                            "total_search": row[1],
                            "direct_search": row[2],
                            "indirect_search": row[3],
                            "total_show": row[4],
                            "via_search_show": row[5],
                            "via_map_show": row[6],
                            "total_action": row[7],
                            "access_website": row[8],
                            "look_map": row[9],
                            "call": row[10],
                        }
                    )
        else:
            print('failur')
