from django.db import models
# from django.utils import timezone


# Create your models here.


class Fes_hp_scrape(models.Model):
    # title = models.CharField(max_length=100)
    month_key = models.CharField(max_length=20, blank=True, null=True)
    date = models.DateField(null=True)
    week = models.CharField(max_length=10, null=True)
    pv_all_sp = models.IntegerField(null=True)
    pv_top_sp = models.IntegerField(null=True)
    pv_coupon_sp = models.IntegerField(null=True)
    cvr_sp = models.CharField(max_length=10, null=True)
    tell_sp = models.IntegerField(null=True)
    reserve_sp = models.IntegerField(null=True)
    reserve_hp = models.IntegerField(null=True)
    reserve_homepage = models.IntegerField(null=True)
    day_over_day_changes = models.IntegerField(null=True)

    def __str__(self):
        return str(self.date)

    class Meta:
        verbose_name = "FES_HP"
        verbose_name_plural = "FES_HP"


class Grg_hp_scrape(models.Model):
    # title = models.CharField(max_length=100)
    month_key = models.CharField(max_length=20, blank=True, null=True)
    date = models.DateField(null=True)
    week = models.CharField(max_length=10, null=True)
    pv_all_sp = models.IntegerField(null=True)
    pv_top_sp = models.IntegerField(null=True)
    pv_coupon_sp = models.IntegerField(null=True)
    cvr_sp = models.CharField(max_length=10, null=True)
    tell_sp = models.IntegerField(null=True)
    reserve_sp = models.IntegerField(null=True)
    reserve_hp = models.IntegerField(null=True)
    reserve_homepage = models.IntegerField(null=True)
    day_over_day_changes = models.IntegerField(null=True)

    def __str__(self):
        return str(self.date)

    class Meta:
        verbose_name = "Garage_HP"
        verbose_name_plural = "Garage_HP"


class Toro_hp_scrape(models.Model):
    # title = models.CharField(max_length=100)
    month_key = models.CharField(max_length=20, blank=True, null=True)
    date = models.DateField(null=True)
    week = models.CharField(max_length=10, null=True)
    pv_all_sp = models.IntegerField(null=True)
    pv_top_sp = models.IntegerField(null=True)
    pv_coupon_sp = models.IntegerField(null=True)
    cvr_sp = models.CharField(max_length=10, null=True)
    tell_sp = models.IntegerField(null=True)
    reserve_sp = models.IntegerField(null=True)
    reserve_hp = models.IntegerField(null=True)
    reserve_homepage = models.IntegerField(null=True)
    day_over_day_changes = models.IntegerField(null=True)

    def __str__(self):
        return str(self.date)

    class Meta:
        verbose_name = "灯篭_HP"
        verbose_name_plural = "灯篭_HP"


class Wana_hp_scrape(models.Model):
    # title = models.CharField(max_length=100)
    month_key = models.CharField(max_length=20, blank=True, null=True)
    date = models.DateField(null=True)
    week = models.CharField(max_length=10, null=True)
    pv_all_sp = models.IntegerField(null=True)
    pv_top_sp = models.IntegerField(null=True)
    pv_coupon_sp = models.IntegerField(null=True)
    cvr_sp = models.CharField(max_length=10, null=True)
    tell_sp = models.IntegerField(null=True)
    reserve_sp = models.IntegerField(null=True)
    reserve_hp = models.IntegerField(null=True)
    reserve_homepage = models.IntegerField(null=True)
    day_over_day_changes = models.IntegerField(null=True)

    def __str__(self):
        return str(self.date)

    class Meta:
        verbose_name = "罠一目_HP"
        verbose_name_plural = "罠一目_HP"


class Wananakame_hp_scrape(models.Model):
    # title = models.CharField(max_length=100)
    month_key = models.CharField(max_length=20, blank=True, null=True)
    date = models.DateField(null=True)
    week = models.CharField(max_length=10, null=True)
    pv_all_sp = models.IntegerField(null=True)
    pv_top_sp = models.IntegerField(null=True)
    pv_coupon_sp = models.IntegerField(null=True)
    cvr_sp = models.CharField(max_length=10, null=True)
    tell_sp = models.IntegerField(null=True)
    reserve_sp = models.IntegerField(null=True)
    reserve_hp = models.IntegerField(null=True)
    reserve_homepage = models.IntegerField(null=True)
    day_over_day_changes = models.IntegerField(null=True)

    def __str__(self):
        return str(self.date)

    class Meta:
        verbose_name = "罠中目黒_HP"
        verbose_name_plural = "罠中目黒_HP"


class Fes_gn_scrape(models.Model):
    # title = models.CharField(max_length=100)
    month_key = models.CharField(max_length=20, blank=True, null=True)
    date = models.DateField(null=True)
    week = models.CharField(max_length=10, null=True)
    total_pv_sp = models.IntegerField("合計PV_SP", null=True)
    top_pv_sp = models.IntegerField("店舗トップPV_SP", null=True)
    menu_pv_sp = models.IntegerField("メニューPV_SP", null=True)
    seat_pv_sp = models.IntegerField("席個室貸切PV_SP", null=True)
    photo_pv_sp = models.IntegerField("写真PV_SP", null=True)
    commitment_pv_sp = models.IntegerField("こだわりPV_SP", null=True)
    map_pv_sp = models.IntegerField("地図PV_SP", null=True)
    coupon_pv_sp = models.IntegerField("クーポンPV_SP", null=True)
    reserve_pv_sp = models.IntegerField("予約PV_SP", null=True)
    total_pv_pc = models.IntegerField("合計PV_PC", null=True)
    top_pv_pc = models.IntegerField("店舗トップPV_PC", null=True)
    menu_pv_pc = models.IntegerField("メニューPV_PC", null=True)
    seat_pv_pc = models.IntegerField("席個室貸切PV_PC", null=True)
    photo_pv_pc = models.IntegerField("写真PV_PC", null=True)
    commitment_pv_pc = models.IntegerField("こだわりPV_PC", null=True)
    map_pv_pc = models.IntegerField("地図PV_PC", null=True)
    coupon_pv_pc = models.IntegerField("クーポンPV_PC", null=True)
    reserve_pv_pc = models.IntegerField("予約PV_PC", null=True)
    total_pv_app = models.IntegerField("合計PV_app", null=True)
    top_pv_app = models.IntegerField("店舗トップPV_app", null=True)
    menu_pv_app = models.IntegerField("メニューPV_app", null=True)
    seat_pv_app = models.IntegerField("席個室貸切PV_app", null=True)
    photo_pv_app = models.IntegerField("写真PV_app", null=True)
    commitment_pv_app = models.IntegerField("こだわりPV_app", null=True)
    map_pv_app = models.IntegerField("地図PV_app", null=True)
    coupon_pv_app = models.IntegerField("クーポンPV_app", null=True)
    reserve_pv_app = models.IntegerField("予約PV_app", null=True)
    reserve_course_number = models.IntegerField("予約_コース_件数", null=True)
    reserve_course_people = models.IntegerField("予約_コース_人数", null=True)
    reserve_course_price = models.IntegerField("予約_コース_金額", null=True)
    reserve_seatonly_number = models.IntegerField("予約_席のみ_件数", null=True)
    reserve_seatonly_people = models.IntegerField("予約_席のみ_人数", null=True)
    reserve_request_number = models.IntegerField("予約_リクエスト_件数", null=True)
    reserve_request_people = models.IntegerField("予約_リクエスト_人数", null=True)
    reserve_total = models.IntegerField("予約_合計件数", null=True)



    def __str__(self):
        return str(self.date)

    class Meta:
        verbose_name = "FES_ぐる"
        verbose_name_plural = "FES_ぐる"


class Grg_gn_scrape(models.Model):
    # title = models.CharField(max_length=100)
    month_key = models.CharField(max_length=20, blank=True, null=True)
    date = models.DateField(null=True)
    week = models.CharField(max_length=10, null=True)
    total_pv_sp = models.IntegerField("合計PV_SP", null=True)
    top_pv_sp = models.IntegerField("店舗トップPV_SP", null=True)
    menu_pv_sp = models.IntegerField("メニューPV_SP", null=True)
    seat_pv_sp = models.IntegerField("席個室貸切PV_SP", null=True)
    photo_pv_sp = models.IntegerField("写真PV_SP", null=True)
    commitment_pv_sp = models.IntegerField("こだわりPV_SP", null=True)
    map_pv_sp = models.IntegerField("地図PV_SP", null=True)
    coupon_pv_sp = models.IntegerField("クーポンPV_SP", null=True)
    reserve_pv_sp = models.IntegerField("予約PV_SP", null=True)
    total_pv_pc = models.IntegerField("合計PV_PC", null=True)
    top_pv_pc = models.IntegerField("店舗トップPV_PC", null=True)
    menu_pv_pc = models.IntegerField("メニューPV_PC", null=True)
    seat_pv_pc = models.IntegerField("席個室貸切PV_PC", null=True)
    photo_pv_pc = models.IntegerField("写真PV_PC", null=True)
    commitment_pv_pc = models.IntegerField("こだわりPV_PC", null=True)
    map_pv_pc = models.IntegerField("地図PV_PC", null=True)
    coupon_pv_pc = models.IntegerField("クーポンPV_PC", null=True)
    reserve_pv_pc = models.IntegerField("予約PV_PC", null=True)
    total_pv_app = models.IntegerField("合計PV_app", null=True)
    top_pv_app = models.IntegerField("店舗トップPV_app", null=True)
    menu_pv_app = models.IntegerField("メニューPV_app", null=True)
    seat_pv_app = models.IntegerField("席個室貸切PV_app", null=True)
    photo_pv_app = models.IntegerField("写真PV_app", null=True)
    commitment_pv_app = models.IntegerField("こだわりPV_app", null=True)
    map_pv_app = models.IntegerField("地図PV_app", null=True)
    coupon_pv_app = models.IntegerField("クーポンPV_app", null=True)
    reserve_pv_app = models.IntegerField("予約PV_app", null=True)
    reserve_course_number = models.IntegerField("予約_コース_件数", null=True)
    reserve_course_people = models.IntegerField("予約_コース_人数", null=True)
    reserve_course_price = models.IntegerField("予約_コース_金額", null=True)
    reserve_seatonly_number = models.IntegerField("予約_席のみ_件数", null=True)
    reserve_seatonly_people = models.IntegerField("予約_席のみ_人数", null=True)
    reserve_request_number = models.IntegerField("予約_リクエスト_件数", null=True)
    reserve_request_people = models.IntegerField("予約_リクエスト_人数", null=True)
    reserve_total = models.IntegerField("予約_合計件数", null=True)


    def __str__(self):
        return str(self.date)

    class Meta:
        verbose_name = "Garage_ぐる"
        verbose_name_plural = "Garage_ぐる"


class Toro_gn_scrape(models.Model):
    # title = models.CharField(max_length=100)
    month_key = models.CharField(max_length=20, blank=True, null=True)
    date = models.DateField(null=True)
    week = models.CharField(max_length=10, null=True)
    total_pv_sp = models.IntegerField("合計PV_SP", null=True)
    top_pv_sp = models.IntegerField("店舗トップPV_SP", null=True)
    menu_pv_sp = models.IntegerField("メニューPV_SP", null=True)
    seat_pv_sp = models.IntegerField("席個室貸切PV_SP", null=True)
    photo_pv_sp = models.IntegerField("写真PV_SP", null=True)
    commitment_pv_sp = models.IntegerField("こだわりPV_SP", null=True)
    map_pv_sp = models.IntegerField("地図PV_SP", null=True)
    coupon_pv_sp = models.IntegerField("クーポンPV_SP", null=True)
    reserve_pv_sp = models.IntegerField("予約PV_SP", null=True)
    total_pv_pc = models.IntegerField("合計PV_PC", null=True)
    top_pv_pc = models.IntegerField("店舗トップPV_PC", null=True)
    menu_pv_pc = models.IntegerField("メニューPV_PC", null=True)
    seat_pv_pc = models.IntegerField("席個室貸切PV_PC", null=True)
    photo_pv_pc = models.IntegerField("写真PV_PC", null=True)
    commitment_pv_pc = models.IntegerField("こだわりPV_PC", null=True)
    map_pv_pc = models.IntegerField("地図PV_PC", null=True)
    coupon_pv_pc = models.IntegerField("クーポンPV_PC", null=True)
    reserve_pv_pc = models.IntegerField("予約PV_PC", null=True)
    total_pv_app = models.IntegerField("合計PV_app", null=True)
    top_pv_app = models.IntegerField("店舗トップPV_app", null=True)
    menu_pv_app = models.IntegerField("メニューPV_app", null=True)
    seat_pv_app = models.IntegerField("席個室貸切PV_app", null=True)
    photo_pv_app = models.IntegerField("写真PV_app", null=True)
    commitment_pv_app = models.IntegerField("こだわりPV_app", null=True)
    map_pv_app = models.IntegerField("地図PV_app", null=True)
    coupon_pv_app = models.IntegerField("クーポンPV_app", null=True)
    reserve_pv_app = models.IntegerField("予約PV_app", null=True)
    reserve_course_number = models.IntegerField("予約_コース_件数", null=True)
    reserve_course_people = models.IntegerField("予約_コース_人数", null=True)
    reserve_course_price = models.IntegerField("予約_コース_金額", null=True)
    reserve_seatonly_number = models.IntegerField("予約_席のみ_件数", null=True)
    reserve_seatonly_people = models.IntegerField("予約_席のみ_人数", null=True)
    reserve_request_number = models.IntegerField("予約_リクエスト_件数", null=True)
    reserve_request_people = models.IntegerField("予約_リクエスト_人数", null=True)
    reserve_total = models.IntegerField("予約_合計件数", null=True)


    def __str__(self):
        return str(self.date)

    class Meta:
        verbose_name = "灯篭_ぐる"
        verbose_name_plural = "灯篭_ぐる"


class Wana_gn_scrape(models.Model):
    # title = models.CharField(max_length=100)
    month_key = models.CharField(max_length=20, blank=True, null=True)
    date = models.DateField(null=True)
    week = models.CharField(max_length=10, null=True)
    total_pv_sp = models.IntegerField("合計PV_SP", null=True)
    top_pv_sp = models.IntegerField("店舗トップPV_SP", null=True)
    menu_pv_sp = models.IntegerField("メニューPV_SP", null=True)
    seat_pv_sp = models.IntegerField("席個室貸切PV_SP", null=True)
    photo_pv_sp = models.IntegerField("写真PV_SP", null=True)
    commitment_pv_sp = models.IntegerField("こだわりPV_SP", null=True)
    map_pv_sp = models.IntegerField("地図PV_SP", null=True)
    coupon_pv_sp = models.IntegerField("クーポンPV_SP", null=True)
    reserve_pv_sp = models.IntegerField("予約PV_SP", null=True)
    total_pv_pc = models.IntegerField("合計PV_PC", null=True)
    top_pv_pc = models.IntegerField("店舗トップPV_PC", null=True)
    menu_pv_pc = models.IntegerField("メニューPV_PC", null=True)
    seat_pv_pc = models.IntegerField("席個室貸切PV_PC", null=True)
    photo_pv_pc = models.IntegerField("写真PV_PC", null=True)
    commitment_pv_pc = models.IntegerField("こだわりPV_PC", null=True)
    map_pv_pc = models.IntegerField("地図PV_PC", null=True)
    coupon_pv_pc = models.IntegerField("クーポンPV_PC", null=True)
    reserve_pv_pc = models.IntegerField("予約PV_PC", null=True)
    total_pv_app = models.IntegerField("合計PV_app", null=True)
    top_pv_app = models.IntegerField("店舗トップPV_app", null=True)
    menu_pv_app = models.IntegerField("メニューPV_app", null=True)
    seat_pv_app = models.IntegerField("席個室貸切PV_app", null=True)
    photo_pv_app = models.IntegerField("写真PV_app", null=True)
    commitment_pv_app = models.IntegerField("こだわりPV_app", null=True)
    map_pv_app = models.IntegerField("地図PV_app", null=True)
    coupon_pv_app = models.IntegerField("クーポンPV_app", null=True)
    reserve_pv_app = models.IntegerField("予約PV_app", null=True)
    reserve_course_number = models.IntegerField("予約_コース_件数", null=True)
    reserve_course_people = models.IntegerField("予約_コース_人数", null=True)
    reserve_course_price = models.IntegerField("予約_コース_金額", null=True)
    reserve_seatonly_number = models.IntegerField("予約_席のみ_件数", null=True)
    reserve_seatonly_people = models.IntegerField("予約_席のみ_人数", null=True)
    reserve_request_number = models.IntegerField("予約_リクエスト_件数", null=True)
    reserve_request_people = models.IntegerField("予約_リクエスト_人数", null=True)
    reserve_total = models.IntegerField("予約_合計件数", null=True)


    def __str__(self):
        return str(self.date)

    class Meta:
        verbose_name = "罠一目_ぐる"
        verbose_name_plural = "罠一目_ぐる"


class Wananakame_gn_scrape(models.Model):
    # title = models.CharField(max_length=100)
    month_key = models.CharField(max_length=20, blank=True, null=True)
    date = models.DateField(null=True)
    week = models.CharField(max_length=10, null=True)
    total_pv_sp = models.IntegerField("合計PV_SP", null=True)
    top_pv_sp = models.IntegerField("店舗トップPV_SP", null=True)
    menu_pv_sp = models.IntegerField("メニューPV_SP", null=True)
    seat_pv_sp = models.IntegerField("席個室貸切PV_SP", null=True)
    photo_pv_sp = models.IntegerField("写真PV_SP", null=True)
    commitment_pv_sp = models.IntegerField("こだわりPV_SP", null=True)
    map_pv_sp = models.IntegerField("地図PV_SP", null=True)
    coupon_pv_sp = models.IntegerField("クーポンPV_SP", null=True)
    reserve_pv_sp = models.IntegerField("予約PV_SP", null=True)
    total_pv_pc = models.IntegerField("合計PV_PC", null=True)
    top_pv_pc = models.IntegerField("店舗トップPV_PC", null=True)
    menu_pv_pc = models.IntegerField("メニューPV_PC", null=True)
    seat_pv_pc = models.IntegerField("席個室貸切PV_PC", null=True)
    photo_pv_pc = models.IntegerField("写真PV_PC", null=True)
    commitment_pv_pc = models.IntegerField("こだわりPV_PC", null=True)
    map_pv_pc = models.IntegerField("地図PV_PC", null=True)
    coupon_pv_pc = models.IntegerField("クーポンPV_PC", null=True)
    reserve_pv_pc = models.IntegerField("予約PV_PC", null=True)
    total_pv_app = models.IntegerField("合計PV_app", null=True)
    top_pv_app = models.IntegerField("店舗トップPV_app", null=True)
    menu_pv_app = models.IntegerField("メニューPV_app", null=True)
    seat_pv_app = models.IntegerField("席個室貸切PV_app", null=True)
    photo_pv_app = models.IntegerField("写真PV_app", null=True)
    commitment_pv_app = models.IntegerField("こだわりPV_app", null=True)
    map_pv_app = models.IntegerField("地図PV_app", null=True)
    coupon_pv_app = models.IntegerField("クーポンPV_app", null=True)
    reserve_pv_app = models.IntegerField("予約PV_app", null=True)
    reserve_course_number = models.IntegerField("予約_コース_件数", null=True)
    reserve_course_people = models.IntegerField("予約_コース_人数", null=True)
    reserve_course_price = models.IntegerField("予約_コース_金額", null=True)
    reserve_seatonly_number = models.IntegerField("予約_席のみ_件数", null=True)
    reserve_seatonly_people = models.IntegerField("予約_席のみ_人数", null=True)
    reserve_request_number = models.IntegerField("予約_リクエスト_件数", null=True)
    reserve_request_people = models.IntegerField("予約_リクエスト_人数", null=True)
    reserve_total = models.IntegerField("予約_合計件数", null=True)


    def __str__(self):
        return str(self.date)

    class Meta:
        verbose_name = "罠中目黒_ぐる"
        verbose_name_plural = "罠中目黒_ぐる"


class Fes_tb_scrape(models.Model):
    # title = models.CharField(max_length=100)
    month_key = models.CharField(max_length=20, blank=True, null=True)
    date = models.DateField(null=True)
    week = models.CharField(max_length=10, null=True)
    top = models.IntegerField(null=True)
    photo = models.IntegerField(null=True)
    photo_info = models.IntegerField(null=True)
    rating = models.IntegerField(null=True)
    menu = models.IntegerField(null=True)
    map = models.IntegerField(null=True)
    coupon = models.IntegerField(null=True)
    p_coupon = models.IntegerField(null=True)
    seat = models.IntegerField(null=True)
    other = models.IntegerField(null=True)
    total = models.IntegerField(null=True)

    def __str__(self):
        return str(self.date)

    class Meta:
        verbose_name = "FES_食べ"
        verbose_name_plural = "FES_食べ"


class Grg_tb_scrape(models.Model):
    # title = models.CharField(max_length=100)
    month_key = models.CharField(max_length=20, blank=True, null=True)
    date = models.DateField(null=True)
    week = models.CharField(max_length=10, null=True)
    top = models.IntegerField(null=True)
    photo = models.IntegerField(null=True)
    photo_info = models.IntegerField(null=True)
    rating = models.IntegerField(null=True)
    menu = models.IntegerField(null=True)
    map = models.IntegerField(null=True)
    coupon = models.IntegerField(null=True)
    p_coupon = models.IntegerField(null=True)
    seat = models.IntegerField(null=True)
    other = models.IntegerField(null=True)
    total = models.IntegerField(null=True)

    def __str__(self):
        return str(self.date)

    class Meta:
        verbose_name = "Garage_食べ"
        verbose_name_plural = "Garage_食べ"


class Toro_tb_scrape(models.Model):
    # title = models.CharField(max_length=100)
    month_key = models.CharField(max_length=20, blank=True, null=True)
    date = models.DateField(null=True)
    week = models.CharField(max_length=10, null=True)
    top = models.IntegerField(null=True)
    photo = models.IntegerField(null=True)
    photo_info = models.IntegerField(null=True)
    rating = models.IntegerField(null=True)
    menu = models.IntegerField(null=True)
    map = models.IntegerField(null=True)
    coupon = models.IntegerField(null=True)
    p_coupon = models.IntegerField(null=True)
    seat = models.IntegerField(null=True)
    other = models.IntegerField(null=True)
    total = models.IntegerField(null=True)

    def __str__(self):
        return str(self.date)

    class Meta:
        verbose_name = "灯篭_食べ"
        verbose_name_plural = "灯篭_食べ"


class Wana_tb_scrape(models.Model):
    # title = models.CharField(max_length=100)
    month_key = models.CharField(max_length=20, blank=True, null=True)
    date = models.DateField(null=True)
    week = models.CharField(max_length=10, null=True)
    top = models.IntegerField(null=True)
    photo = models.IntegerField(null=True)
    photo_info = models.IntegerField(null=True)
    rating = models.IntegerField(null=True)
    menu = models.IntegerField(null=True)
    map = models.IntegerField(null=True)
    coupon = models.IntegerField(null=True)
    p_coupon = models.IntegerField(null=True)
    seat = models.IntegerField(null=True)
    other = models.IntegerField(null=True)
    total = models.IntegerField(null=True)

    def __str__(self):
        return str(self.date)

    class Meta:
        verbose_name = "罠一目_食べ"
        verbose_name_plural = "罠一目_食べ"


class Wananakame_tb_scrape(models.Model):
    # title = models.CharField(max_length=100)
    month_key = models.CharField(max_length=20, blank=True, null=True)
    date = models.DateField(null=True)
    week = models.CharField(max_length=10, null=True)
    top = models.IntegerField(null=True)
    photo = models.IntegerField(null=True)
    photo_info = models.IntegerField(null=True)
    rating = models.IntegerField(null=True)
    menu = models.IntegerField(null=True)
    map = models.IntegerField(null=True)
    coupon = models.IntegerField(null=True)
    p_coupon = models.IntegerField(null=True)
    seat = models.IntegerField(null=True)
    other = models.IntegerField(null=True)
    total = models.IntegerField(null=True)

    def __str__(self):
        return str(self.date)

    class Meta:
        verbose_name = "罠中目黒_食べ"
        verbose_name_plural = "罠中目黒_食べ"


class Fes_GMB(models.Model):
    # title = models.CharField(max_length=100)
    span_id = models.CharField("期間ID", default='0', max_length=20, blank=False, null=False)
    span = models.CharField("期間", max_length=20, blank=False, null=False, primary_key=True)
    total_evaluation = models.FloatField("総合評価", blank=True, null=True)
    total_search = models.IntegerField("合計検索数", blank=True, null=True)
    direct_search = models.IntegerField("直接検索数", blank=True,  null=True)
    indirect_search = models.IntegerField("間接検索数", blank=True,  null=True)
    total_show = models.IntegerField("合計表示回数", blank=True,  null=True)
    via_search_show = models.IntegerField("検索経由の閲覧数", blank=True,  null=True)
    via_map_show = models.IntegerField("マップ経由の閲覧数", blank=True,  null=True)
    total_action = models.IntegerField("合計反応数", blank=True,  null=True)
    access_website = models.IntegerField("ウェブサイトへのアクセス数", blank=True,  null=True)
    look_map = models.IntegerField("ルートの照会数", blank=True,  null=True)
    call = models.IntegerField("通話数", blank=True,  null=True)

    def __str__(self):
        return str(self.span)

    class Meta:
        verbose_name = "FES_GMB"
        verbose_name_plural = "FES_GMB"


class Grg_GMB(models.Model):
    # title = models.CharField(max_length=100)
    span_id = models.CharField("期間ID", default='0', max_length=20, blank=False, null=False)
    span = models.CharField("期間", max_length=20, blank=False, null=False, primary_key=True)
    total_evaluation = models.FloatField("総合評価", blank=True, null=True)
    total_search = models.IntegerField("合計検索数", blank=True, null=True)
    direct_search = models.IntegerField("直接検索数", blank=True,  null=True)
    indirect_search = models.IntegerField("間接検索数", blank=True,  null=True)
    total_show = models.IntegerField("合計表示回数", blank=True,  null=True)
    via_search_show = models.IntegerField("検索経由の閲覧数", blank=True,  null=True)
    via_map_show = models.IntegerField("マップ経由の閲覧数", blank=True,  null=True)
    total_action = models.IntegerField("合計反応数", blank=True,  null=True)
    access_website = models.IntegerField("ウェブサイトへのアクセス数", blank=True,  null=True)
    look_map = models.IntegerField("ルートの照会数", blank=True,  null=True)
    call = models.IntegerField("通話数", blank=True,  null=True)

    def __str__(self):
        return str(self.span)

    class Meta:
        verbose_name = "Garage_GMB"
        verbose_name_plural = "Garage_GMB"


class Toro_GMB(models.Model):
    # title = models.CharField(max_length=100)
    span_id = models.CharField("期間ID", default='0', max_length=20, blank=False, null=False)
    span = models.CharField("期間", max_length=20, blank=False, null=False, primary_key=True)
    total_evaluation = models.FloatField("総合評価", blank=True, null=True)
    total_search = models.IntegerField("合計検索数", blank=True, null=True)
    direct_search = models.IntegerField("直接検索数", blank=True,  null=True)
    indirect_search = models.IntegerField("間接検索数", blank=True,  null=True)
    total_show = models.IntegerField("合計表示回数", blank=True,  null=True)
    via_search_show = models.IntegerField("検索経由の閲覧数", blank=True,  null=True)
    via_map_show = models.IntegerField("マップ経由の閲覧数", blank=True,  null=True)
    total_action = models.IntegerField("合計反応数", blank=True,  null=True)
    access_website = models.IntegerField("ウェブサイトへのアクセス数", blank=True,  null=True)
    look_map = models.IntegerField("ルートの照会数", blank=True,  null=True)
    call = models.IntegerField("通話数", blank=True,  null=True)

    def __str__(self):
        return str(self.span)

    class Meta:
        verbose_name = "灯篭_GMB"
        verbose_name_plural = "灯篭_GMB"


class Wanaichi_GMB(models.Model):
    # title = models.CharField(max_length=100)
    span_id = models.CharField("期間ID", default='0', max_length=20, blank=False, null=False)
    span = models.CharField("期間", max_length=20, blank=False, null=False, primary_key=True)
    total_evaluation = models.FloatField("総合評価", blank=True, null=True)
    total_search = models.IntegerField("合計検索数", blank=True, null=True)
    direct_search = models.IntegerField("直接検索数", blank=True,  null=True)
    indirect_search = models.IntegerField("間接検索数", blank=True,  null=True)
    total_show = models.IntegerField("合計表示回数", blank=True,  null=True)
    via_search_show = models.IntegerField("検索経由の閲覧数", blank=True,  null=True)
    via_map_show = models.IntegerField("マップ経由の閲覧数", blank=True,  null=True)
    total_action = models.IntegerField("合計反応数", blank=True,  null=True)
    access_website = models.IntegerField("ウェブサイトへのアクセス数", blank=True,  null=True)
    look_map = models.IntegerField("ルートの照会数", blank=True,  null=True)
    call = models.IntegerField("通話数", blank=True,  null=True)

    def __str__(self):
        return str(self.span)

    class Meta:
        verbose_name = "罠一目_GMB"
        verbose_name_plural = "罠一目_GMB"


class Wananakame_GMB(models.Model):
    # title = models.CharField(max_length=100)
    span_id = models.CharField("期間ID", default='0', max_length=20, blank=False, null=False)
    span = models.CharField("期間", max_length=20, blank=False, null=False, primary_key=True)
    total_evaluation = models.FloatField("総合評価", blank=True, null=True)
    total_search = models.IntegerField("合計検索数", blank=True, null=True)
    direct_search = models.IntegerField("直接検索数", blank=True,  null=True)
    indirect_search = models.IntegerField("間接検索数", blank=True,  null=True)
    total_show = models.IntegerField("合計表示回数", blank=True,  null=True)
    via_search_show = models.IntegerField("検索経由の閲覧数", blank=True,  null=True)
    via_map_show = models.IntegerField("マップ経由の閲覧数", blank=True,  null=True)
    total_action = models.IntegerField("合計反応数", blank=True,  null=True)
    access_website = models.IntegerField("ウェブサイトへのアクセス数", blank=True,  null=True)
    look_map = models.IntegerField("ルートの照会数", blank=True,  null=True)
    call = models.IntegerField("通話数", blank=True,  null=True)

    def __str__(self):
        return str(self.span)

    class Meta:
        verbose_name = "罠中目黒_GMB"
        verbose_name_plural = "罠中目黒_GMB"
