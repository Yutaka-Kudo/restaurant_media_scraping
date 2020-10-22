from django.contrib import admin
from .models import Fes_hp_sp_scrape
# Register your models here.

class Fes_hp_sp_scrapeAdmin(admin.ModelAdmin):
    list_display = ("date", "week")


admin.site.register(Fes_hp_sp_scrape, Fes_hp_sp_scrapeAdmin)