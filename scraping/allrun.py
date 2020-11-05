from . import fes_gn, fes_hp, fes_tb, grg_gn, grg_hp, grg_tb, toro_gn, toro_hp, toro_tb, wana_gn, wana_hp, wana_tb
from django.shortcuts import render, redirect


# fes_gn.fes_gn_sp()
def allrun(request):
    # fes_gn.fes_gn_sp(request)
    # fes_hp.fes_hp_sp(request)
    # fes_tb.fes_tb_sp(request)

    # grg_gn.grg_gn_sp(request)
    # grg_hp.grg_hp_sp(request)
    # grg_tb.grg_tb_sp(request)

    # toro_gn.toro_gn_sp(request)
    toro_hp.toro_hp_sp(request)
    # toro_tb.toro_tb_sp(request)

    # wana_gn.wana_gn_sp(request)
    wana_hp.wana_hp_sp(request)
    # wana_tb.wana_tb_sp(request)

    return redirect("/dev/")


