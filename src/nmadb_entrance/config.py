from django.forms.models import model_to_dict


class Info(object):
    """ Session information object.
    """

    def __init__(self):
        self.session_is_program_based = False
        self._info_object = None

    def as_dict(self):
        """ Returns data as Python dictionary.
        """
        return model_to_dict(self._info, fields=[], exclude=[])

    def __getattr__(self, name):
        return getattr(self._info, name)

    @property
    def _info(self):
        """ Returns the info object.
        """
        if self._info_object is None:
            self._info_object = self._get_info_object()
        return self._info_object

    def _get_info_object(self):
        """ Gets or crates the info object.
        """
        from nmadb_entrance.models import Info

        try:
            info = Info.objects.all()[0]
        except IndexError:
            import datetime
            info = Info()
            info.address = (
                    u'Student\u0173 g. 63a-206, Kaunas LT-51369')
            info.address_multiline = u'''
            V\u0161\u012e \u201eNacionalin\u0117 moksleivi\u0173 akademija\u201c
            Student\u0173 g. 63A-206
            LT-51369 Kaunas
        '''
            info.year = 2012
            info.forms_send_deadline = datetime.date(2012, 9, 20)
            info.manager_name_dative = u'R\u016btai'
            info.manager_email = u'info@nmakademija.lt'
            info.manager_phone = u'+37067768899'
            info.admin_email = u'atranka@nmakademija.lt'
            info.pupil_form_deadline = datetime.date(2012, 9, 16)
            info.pupil_pay_deadline = datetime.date(2012, 9, 16)
            info.entrance_fee = 30
            info.firm_title = (
                    u'Vie\u0161oji \u012fstaiga \u201eNacionalin\u0117 '
                    u'moksleivi\u0173 akademija\u201c')
            info.firm_code = u'\u012e.k. 300628321'
            info.bank_account = u'A/S LT197300010104583271'
            info.success_notification_deadline = datetime.date(2012, 10, 7)
            info.save()
        finally:
            del Info
            return info


info = Info()
