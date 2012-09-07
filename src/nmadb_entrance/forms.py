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
        model = models.RegistrationInfo
        fields = (
                'first_name',
                'last_name',
                'gender',
                'school',
                'email',
                'section',
                'school_class',
                )


class PupilInfoForm(forms.ModelForm):
    """ Form for pupil.
    """

    class Meta(object):
        model = models.PupilInfo
        exclude = (
                'base',
                'commit_timestamp',
                'home_address',
                )


class TeacherInfoForm(forms.ModelForm):
    """ Form for teacher.
    """

    social = forms.BooleanField(
            widget=forms.Select(choices=(
                (True, _(u'Yes')),
                (False, _(u'No')),
                )),
            required=False,
            )

    def clean(self):
        """ Checks if at least one of ``form_master``,
        ``subject_teacher`` and ``other_relation`` is set.
        """

        cleaned_data = super(TeacherInfoForm, self).clean()

        if not (cleaned_data['class_master'] or
                cleaned_data['subject_teacher'] or
                cleaned_data['other_relation']):
            raise forms.ValidationError(
                    _(u'You have to specify Your relation with pupil.'))

        return cleaned_data

    class Meta(object):
        model = models.TeacherInfo
        exclude = ('base', 'commit_timestamp',)


class DirectorInfoForm(forms.ModelForm):
    """ Form for director.
    """

    social = forms.BooleanField(
            widget=forms.Select(choices=(
                (True, _(u'Yes')),
                (False, _(u'No')),
                )),
            required=False,
            )

    class Meta(object):
        model = models.DirectorInfo
        exclude = ('base', 'commit_timestamp',)
