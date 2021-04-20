from devtools import debug
from scraping.models import *
import datetime


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


def trans_date(i):  # 0000-00-00の形
    if type(i) == str:
        result = datetime.datetime.strptime(i, '%Y-%m-%d').date()
    elif type(i) == datetime.date:
        result = datetime.date.strftime(i, '%Y-%m-%d')
    return result


def addtax_elementText(elem, tax_rate: float = 1.1):
    """
    渡したエレメントのテキスト内の
    「0000円」を→「0000円(税込0,000円)」
    """
    value = elem.get_attribute('value')
    index_num_list = [n for n, v in enumerate(value) if v == "円"]
    if index_num_list:
        for cursor in reversed(index_num_list):  # リバースしないと修正が上書きされる 1箇所ずつ原文を処理してるため長さが変わるから enumerateで先頭からの番号を出してるから
            st_cursor = cursor-1
            try:
                while type(int(value[st_cursor])) == int:
                    st_cursor -= 1
                    if value[st_cursor] == ",":
                        st_cursor -= 1
            except Exception:  # 上のtryをやり尽くしたら
                old_price = value[st_cursor+1:cursor].replace(',', '')
                new_price = (int(old_price)*tax_rate)
                new_sentence = "(税込{:,.0f}円)".format(new_price)
                old_sentence = "{:,.0f}円".format(int(old_price))
                value = value[:st_cursor+1]+old_sentence+new_sentence+value[cursor+1:]
        print(value)
        elem.clear()
        elem.send_keys(value)
