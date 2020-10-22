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
        return self.date


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
        return self.date


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
        return self.date
