from django.contrib import admin
from scraping.models import *

# Register your models here.


class Fes_hp_scrapeAdmin(admin.ModelAdmin):
    list_display = ("date", "week")


admin.site.register(Fes_hp_scrape, Fes_hp_scrapeAdmin)


class Fes_gn_scrapeAdmin(admin.ModelAdmin):
    list_display = ("date", "week")


admin.site.register(Fes_gn_scrape, Fes_gn_scrapeAdmin)


class Fes_tb_scrapeAdmin(admin.ModelAdmin):
    list_display = ("date", "week")


admin.site.register(Fes_tb_scrape, Fes_tb_scrapeAdmin)


class Grg_gn_scrapeAdmin(admin.ModelAdmin):
    list_display = ("date", "week")


admin.site.register(Grg_gn_scrape, Grg_gn_scrapeAdmin)


class Grg_hp_scrapeAdmin(admin.ModelAdmin):
    list_display = ("date", "week")


admin.site.register(Grg_hp_scrape, Grg_hp_scrapeAdmin)


class Grg_tb_scrapeAdmin(admin.ModelAdmin):
    list_display = ("date", "week")


admin.site.register(Grg_tb_scrape, Grg_tb_scrapeAdmin)


class Toro_hp_scrapeAdmin(admin.ModelAdmin):
    list_display = ("date", "week")


admin.site.register(Toro_hp_scrape, Toro_hp_scrapeAdmin)


class Toro_gn_scrapeAdmin(admin.ModelAdmin):
    list_display = ("date", "week")


admin.site.register(Toro_gn_scrape, Toro_gn_scrapeAdmin)


class Toro_tb_scrapeAdmin(admin.ModelAdmin):
    list_display = ("date", "week")


admin.site.register(Toro_tb_scrape, Toro_tb_scrapeAdmin)


class Wana_hp_scrapeAdmin(admin.ModelAdmin):
    list_display = ("date", "week")


admin.site.register(Wana_hp_scrape, Wana_hp_scrapeAdmin)


class Wana_gn_scrapeAdmin(admin.ModelAdmin):
    list_display = ("date", "week")


admin.site.register(Wana_gn_scrape, Wana_gn_scrapeAdmin)


class Wana_tb_scrapeAdmin(admin.ModelAdmin):
    list_display = ("date", "week")


admin.site.register(Wana_tb_scrape, Wana_tb_scrapeAdmin)


class Wananakame_hp_scrapeAdmin(admin.ModelAdmin):
    list_display = ("date", "week")


admin.site.register(Wananakame_hp_scrape, Wananakame_hp_scrapeAdmin)


class Wananakame_gn_scrapeAdmin(admin.ModelAdmin):
    list_display = ("date", "week")


admin.site.register(Wananakame_gn_scrape, Wananakame_gn_scrapeAdmin)


class Wananakame_tb_scrapeAdmin(admin.ModelAdmin):
    list_display = ("date", "week")


admin.site.register(Wananakame_tb_scrape, Wananakame_tb_scrapeAdmin)


class Fes_GMBAdmin(admin.ModelAdmin):
    list_display = ("span", "total_evaluation")


admin.site.register(Fes_GMB, Fes_GMBAdmin)


class Grg_GMBAdmin(admin.ModelAdmin):
    list_display = ("span", "total_evaluation")


admin.site.register(Grg_GMB, Grg_GMBAdmin)


class Toro_GMBAdmin(admin.ModelAdmin):
    list_display = ("span", "total_evaluation")


admin.site.register(Toro_GMB, Toro_GMBAdmin)


class Wanaichi_GMBAdmin(admin.ModelAdmin):
    list_display = ("span", "total_evaluation")


admin.site.register(Wanaichi_GMB, Wanaichi_GMBAdmin)


class Wananakame_GMBAdmin(admin.ModelAdmin):
    list_display = ("span", "total_evaluation")


admin.site.register(Wananakame_GMB, Wananakame_GMBAdmin)
