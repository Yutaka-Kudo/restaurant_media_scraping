from scraping.models import *


def create_dbdict(dbmodel):
    ver_name_list = []
    db_column_list = []
    for i in dir(dbmodel):
        try:
            exec(f"ver_name_list.append({dbmodel.__name__}.{i}.field.verbose_name)")
            db_column_list.append(i)
        except Exception:
            pass
    dbdict = dict(zip(db_column_list, ver_name_list))
    return dbdict
