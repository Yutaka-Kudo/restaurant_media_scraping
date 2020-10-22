from django.db import models
from django.utils import timezone


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
    
    # data = models.FileField
    # file = models.FileField('ファイル')

    # def __str__(self):
    #     return self.file.url
    def __str__(self):
        return self.date

        # content = models.object
