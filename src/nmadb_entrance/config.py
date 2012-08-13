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
    info.save()
