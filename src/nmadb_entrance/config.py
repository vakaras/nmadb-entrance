from nmadb_entrance.models import Info


try:
    info = Info.objects.all()[0]
except IndexError:
    import datetime
    now = datetime.datetime.now()
    info = Info()
    info.address = (
            u'Gedimino pr. 9, Vilnius LT-01103 '
            u'(NVO Avilys, 3 auk\u0161tas)')
    info.year = now.year
    info.forms_send_deadline = now.date() + datetime.timedelta(days=30)
    info.manager_name_dative = u'Vardeniui Pavardeniui'
    info.manager_email = u'vardenis.pavardenis@example.com'
    info.manager_phone = u'+37060000000'
    info.admin_email = u'admin@example.com'
    info.pupil_form_deadline = now.date() + datetime.timedelta(days=28)
    info.entrance_fee = 100
    info.firm_title = 'Some title'
    info.firm_code = 'Some code'
    info.bank_account = 'Some bank account number'
    info.success_notification_deadline = (
            now.date() + datetime.timedelta(days=40))
    info.save()
