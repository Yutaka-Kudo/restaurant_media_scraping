import pandas as pd
import datetime
from scraping.models import *
from scraping.site_package.my_module import create_dbdict
from django.core.management.base import BaseCommand

# csvファイルの名前の文末の謎数字消す前処理、忘れずに

class Command(BaseCommand):  # コマンド python manage.py get_insert_db
    def handle(self, *args, **options):

        start_date = "2021-2-28"
        end_date = datetime.date.strftime(datetime.datetime.strptime(start_date, "%Y-%m-%d").date() + datetime.timedelta(days=6), "%Y-%-m-%-d")
        for_span = start_date + "_" + end_date

        df = pd.read_csv(f'scraping/site_package/GMB insights (Discovery Report) - {start_date} - {end_date} -.csv', index_col="ビジネス名")

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
