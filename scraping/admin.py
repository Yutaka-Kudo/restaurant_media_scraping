from django.contrib import admin
from .models import Fes_hp_sp_scrape
from .models import Fes_gn_sp_scrape
from .models import Fes_tb_sp_scrape
from .models import Grg_gn_sp_scrape
from .models import Grg_hp_sp_scrape
from .models import Grg_tb_sp_scrape
from .models import Toro_gn_sp_scrape
from .models import Toro_hp_sp_scrape
from .models import Toro_tb_sp_scrape
from .models import Wana_gn_sp_scrape
from .models import Wana_hp_sp_scrape
from .models import Wana_tb_sp_scrape
# Register your models here.


class Fes_hp_sp_scrapeAdmin(admin.ModelAdmin):
    list_display = ("date", "week")


admin.site.register(Fes_hp_sp_scrape, Fes_hp_sp_scrapeAdmin)


class Fes_gn_sp_scrapeAdmin(admin.ModelAdmin):
    list_display = ("date", "week")


admin.site.register(Fes_gn_sp_scrape, Fes_gn_sp_scrapeAdmin)


class Fes_tb_sp_scrapeAdmin(admin.ModelAdmin):
    list_display = ("date", "week")


admin.site.register(Fes_tb_sp_scrape, Fes_tb_sp_scrapeAdmin)


class Grg_gn_sp_scrapeAdmin(admin.ModelAdmin):
    list_display = ("date", "week")


admin.site.register(Grg_gn_sp_scrape, Grg_gn_sp_scrapeAdmin)


class Grg_hp_sp_scrapeAdmin(admin.ModelAdmin):
    list_display = ("date", "week")


admin.site.register(Grg_hp_sp_scrape, Grg_hp_sp_scrapeAdmin)


class Grg_tb_sp_scrapeAdmin(admin.ModelAdmin):
    list_display = ("date", "week")


admin.site.register(Grg_tb_sp_scrape, Grg_tb_sp_scrapeAdmin)


class Toro_hp_sp_scrapeAdmin(admin.ModelAdmin):
    list_display = ("date", "week")


admin.site.register(Toro_hp_sp_scrape, Toro_hp_sp_scrapeAdmin)


class Toro_gn_sp_scrapeAdmin(admin.ModelAdmin):
    list_display = ("date", "week")


admin.site.register(Toro_gn_sp_scrape, Toro_gn_sp_scrapeAdmin)


class Toro_tb_sp_scrapeAdmin(admin.ModelAdmin):
    list_display = ("date", "week")


admin.site.register(Toro_tb_sp_scrape, Toro_tb_sp_scrapeAdmin)


class Wana_hp_sp_scrapeAdmin(admin.ModelAdmin):
    list_display = ("date", "week")


admin.site.register(Wana_hp_sp_scrape, Wana_hp_sp_scrapeAdmin)


class Wana_gn_sp_scrapeAdmin(admin.ModelAdmin):
    list_display = ("date", "week")


admin.site.register(Wana_gn_sp_scrape, Wana_gn_sp_scrapeAdmin)


class Wana_tb_sp_scrapeAdmin(admin.ModelAdmin):
    list_display = ("date", "week")


admin.site.register(Wana_tb_sp_scrape, Wana_tb_sp_scrapeAdmin)
