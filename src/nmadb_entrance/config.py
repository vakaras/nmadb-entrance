from nmadb_entrance.models import Info


try:
    info = Info.objects.all()[0]
except IndexError:
    import datetime
    info = Info()
    info.address = (
            u'Student\u0173 g. 63a-206, Kaunas LT-51369')
    info.address_multiline = (
            u'Student\u0173 g. 63a-206,\nKaunas LT-51369')
    info.year = 2012
    info.forms_send_deadline = datetime.date(2012, 9, 20)
    info.manager_name_dative = u'Rūtai'
    info.manager_email = u'info@nmakademija.lt'
    info.manager_phone = u'+37067768899'
    info.admin_email = u'atranka@nmakademija.lt'
    info.pupil_form_deadline = datetime.date(2012, 9, 16)
    info.entrance_fee = 30
    info.firm_title = (
            u'Vie\u0161oji \u012fstaiga \u201eNacionalin\u0117 '
            u'moksleivi\u0173 akademija\u201c'
    info.firm_code = u'\u012e.k. 300628321'
    info.bank_account = u'A/S LT197300010104583271'
    info.success_notification_deadline = datetime.date(2012, 10, 7)
    info.save()
