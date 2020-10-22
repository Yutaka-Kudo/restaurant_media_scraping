basepath, ext = os.path.splitext(os.path.basename(__file__))
now = dt.datetime.now().strftime('%Y%m%d')
oldpath = 'data_fes_tb_sp_{}.csv'.format(now)

response = HttpResponse(content_type='text/csv; charset=UTF-8-sig')
response['Content-Disposition'] = 'attachment; filename={}'.format(oldpath)
df_fix.to_csv(path_or_buf=response, float_format='%.2f', decimal=",")

return response
