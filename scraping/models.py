from django.db import models
# from django.utils import timezone


# Create your models here.


class Fes_hp_sp_scrape(models.Model):
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
        verbose_name = "FES_HP_SP"
        verbose_name_plural = "FES_HP_SP"


class Grg_hp_sp_scrape(models.Model):
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
        verbose_name = "Garage_HP_SP"
        verbose_name_plural = "Garage_HP_SP"


class Toro_hp_sp_scrape(models.Model):
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
        verbose_name = "灯篭_HP_SP"
        verbose_name_plural = "灯篭_HP_SP"


class Wana_hp_sp_scrape(models.Model):
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
        verbose_name = "罠一目_HP_SP"
        verbose_name_plural = "罠一目_HP_SP"


class Wananakame_hp_sp_scrape(models.Model):
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
        verbose_name = "罠中目黒_HP_SP"
        verbose_name_plural = "罠中目黒_HP_SP"


class Fes_gn_sp_scrape(models.Model):
    # title = models.CharField(max_length=100)
    month_key = models.CharField(max_length=20, blank=True, null=True)
    date = models.DateField(null=True)
    week = models.CharField(max_length=10, null=True)
    total = models.IntegerField(null=True)
    top = models.IntegerField(null=True)
    menu = models.IntegerField(null=True)
    seat = models.IntegerField(null=True)
    photo = models.IntegerField(null=True)
    commitment = models.IntegerField(null=True)
    map = models.IntegerField(null=True)
    coupon = models.IntegerField(null=True)
    reserve = models.IntegerField(null=True)

    def __str__(self):
        return str(self.date)

    class Meta:
        verbose_name = "FES_ぐる_SP"
        verbose_name_plural = "FES_ぐる_SP"


class Grg_gn_sp_scrape(models.Model):
    # title = models.CharField(max_length=100)
    month_key = models.CharField(max_length=20, blank=True, null=True)
    date = models.DateField(null=True)
    week = models.CharField(max_length=10, null=True)
    total = models.IntegerField(null=True)
    top = models.IntegerField(null=True)
    menu = models.IntegerField(null=True)
    seat = models.IntegerField(null=True)
    photo = models.IntegerField(null=True)
    commitment = models.IntegerField(null=True)
    map = models.IntegerField(null=True)
    coupon = models.IntegerField(null=True)
    reserve = models.IntegerField(null=True)

    def __str__(self):
        return str(self.date)

    class Meta:
        verbose_name = "Garage_ぐる_SP"
        verbose_name_plural = "Garage_ぐる_SP"


class Toro_gn_sp_scrape(models.Model):
    # title = models.CharField(max_length=100)
    month_key = models.CharField(max_length=20, blank=True, null=True)
    date = models.DateField(null=True)
    week = models.CharField(max_length=10, null=True)
    total = models.IntegerField(null=True)
    top = models.IntegerField(null=True)
    menu = models.IntegerField(null=True)
    seat = models.IntegerField(null=True)
    photo = models.IntegerField(null=True)
    commitment = models.IntegerField(null=True)
    map = models.IntegerField(null=True)
    coupon = models.IntegerField(null=True)
    reserve = models.IntegerField(null=True)

    def __str__(self):
        return str(self.date)

    class Meta:
        verbose_name = "灯篭_ぐる_SP"
        verbose_name_plural = "灯篭_ぐる_SP"


class Wana_gn_sp_scrape(models.Model):
    # title = models.CharField(max_length=100)
    month_key = models.CharField(max_length=20, blank=True, null=True)
    date = models.DateField(null=True)
    week = models.CharField(max_length=10, null=True)
    total = models.IntegerField(null=True)
    top = models.IntegerField(null=True)
    menu = models.IntegerField(null=True)
    seat = models.IntegerField(null=True)
    photo = models.IntegerField(null=True)
    commitment = models.IntegerField(null=True)
    map = models.IntegerField(null=True)
    coupon = models.IntegerField(null=True)
    reserve = models.IntegerField(null=True)

    def __str__(self):
        return str(self.date)

    class Meta:
        verbose_name = "罠一目_ぐる_SP"
        verbose_name_plural = "罠一目_ぐる_SP"


class Wananakame_gn_sp_scrape(models.Model):
    # title = models.CharField(max_length=100)
    month_key = models.CharField(max_length=20, blank=True, null=True)
    date = models.DateField(null=True)
    week = models.CharField(max_length=10, null=True)
    total = models.IntegerField(null=True)
    top = models.IntegerField(null=True)
    menu = models.IntegerField(null=True)
    seat = models.IntegerField(null=True)
    photo = models.IntegerField(null=True)
    commitment = models.IntegerField(null=True)
    map = models.IntegerField(null=True)
    coupon = models.IntegerField(null=True)
    reserve = models.IntegerField(null=True)

    def __str__(self):
        return str(self.date)

    class Meta:
        verbose_name = "罠中目黒_ぐる_SP"
        verbose_name_plural = "罠中目黒_ぐる_SP"


class Fes_tb_sp_scrape(models.Model):
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
        verbose_name = "FES_食べ_SP"
        verbose_name_plural = "FES_食べ_SP"


class Grg_tb_sp_scrape(models.Model):
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
        verbose_name = "Garage_食べ_SP"
        verbose_name_plural = "Garage_食べ_SP"


class Toro_tb_sp_scrape(models.Model):
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
        verbose_name = "灯篭_食べ_SP"
        verbose_name_plural = "灯篭_食べ_SP"


class Wana_tb_sp_scrape(models.Model):
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
        verbose_name = "罠一目_食べ_SP"
        verbose_name_plural = "罠一目_食べ_SP"


class Wananakame_tb_sp_scrape(models.Model):
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
        verbose_name = "罠中目黒_食べ_SP"
        verbose_name_plural = "罠中目黒_食べ_SP"


class Fes_GMB(models.Model):
    # title = models.CharField(max_length=100)
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
