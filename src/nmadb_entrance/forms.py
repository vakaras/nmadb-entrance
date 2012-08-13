from django import forms
from django.utils.translation import ugettext as _

from nmadb_entrance import models
from nmadb_registration.conditions import check_condition


class BaseInfoForm(forms.ModelForm):
    """ Form for entering basic info.
    """

    def clean(self):
        """ Forbids registration.
        """

        super(BaseInfoForm, self).clean()

        cleaned_data = self.cleaned_data

        if check_condition(
                u'registration-ended-custom',
                base_info_cd=cleaned_data):
            raise forms.ValidationError(
                    _(u'Registration ended.'))

        return cleaned_data

    class Meta(object):
        model = models.BaseInfo
        exclude = (
                'uuid',
                'school_year',
                'generated_address',
                'commit_timestamp',
                )
