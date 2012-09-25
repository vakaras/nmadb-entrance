import os
import smtplib

from django.contrib import admin
from django import forms
from django.shortcuts import render
from django.utils.translation import ugettext as _

from nmadb_entrance import models
from nmadb_utils import admin as utils
from nmadb_utils import actions, mail


class BaseInfoAdmin(utils.ModelAdmin):
    """ Administration for base info.
    """

    list_display = (
            'id',
            'first_name',
            'last_name',
            'school',
            'email',
            'section',
            'school_class',
            'generated_address',
            )

    list_filter = (
            'section',
            'school_class',
            )

    search_fields = (
            'id',
            'uuid',
            'first_name',
            'last_name',
            'school__title',
            )

    readonly_fields = (
            'commit_timestamp',
            )


class RegistrationInfoAdmin(utils.ModelAdmin):
    """ Administration for registration info.
    """

    list_display = (
            'id',
            'first_name',
            'last_name',
            'school',
            'school_class',
            'payed',
            'pupil_form_received',
            'teacher_form_received',
            #'director_form_received',
            'marks_form_received',
            'done',
            'testing_location',
            'socialy_supported',
            )

    list_filter = (
            'section',
            'school_class',
            'payed',
            'pupil_form_received',
            'teacher_form_received',
            #'director_form_received',
            'marks_form_received',
            'done',
            'testing_location',
            'socialy_supported',
            )

    search_fields = (
            'id',
            'uuid',
            'first_name',
            'last_name',
            'school__title',
            )

    list_editable = [
            'payed',
            'pupil_form_received',
            'teacher_form_received',
            #'director_form_received',
            'marks_form_received',
            'done',
            'testing_location',
            'socialy_supported',
            ]

    actions = utils.ModelAdmin.actions + [
            'send_mail',
            ]

    class MailForm(forms.Form):
        """ Send mail form.
        """
        _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
        host = forms.CharField(label=_(u'SMTP server'))
        username = forms.EmailField(label=_(u'GMail account'))
                                        # FIXME: Make usable not only
                                        # with GMail.
        password = forms.CharField(
                widget=forms.PasswordInput(), label=_(u'password'))
        port = forms.IntegerField(label=_(u'port'))

        title = forms.CharField(label=_(u'title'))
        text = forms.CharField(widget=forms.Textarea(), label=_(u'text'))

        attachment1_label = forms.CharField(
                required=False, label=u'1 attachment label')
        attachment1 = forms.FileField(
                required=False, label=u'1 attachment')

        attachment2_label = forms.CharField(
                required=False, label=u'2 attachment label')
        attachment2 = forms.FileField(
                required=False, label=u'2 attachment')

        attachment3_label = forms.CharField(
                required=False, label=u'3 attachment label')
        attachment3 = forms.FileField(
                required=False, label=u'3 attachment')

        def clean_password(self):
            """ Checks if password is not too long.
            """

            try:
                password = str(self.cleaned_data['password'])
            except UnicodeEncodeError:
                raise forms.ValidationError((
                    _(u'Server does not support Unicode passwords.')))
            if len(password) > 16:
                raise forms.ValidationError(
                    _(u'Password is longer than 16 symbols.'))
            return password

        def _clean_attachment_label(self, number):
            """ Checks if extension is provided.
            """
            if not self.cleaned_data.get(
                    'attachment{0}_label'.format(number)):
                return u''
            filename, extension = os.path.splitext(
                    self.cleaned_data['attachment{0}_label'.format(number)])
            if not extension:
                raise forms.ValidationError(
                        u'Failed to extract extension from file name.')
            return u'.'.join([filename, extension])

        clean_attachment1_label = (
                lambda self: self._clean_attachment_label(1))
        clean_attachment2_label = (
                lambda self: self._clean_attachment_label(2))
        clean_attachment3_label = (
                lambda self: self._clean_attachment_label(3))

    def send_mail(self, request, queryset):
        """ Allows to send email.
        """
        form = None
        errors = None
        if 'apply' in request.POST:
            form = self.MailForm(request.POST, request.FILES)

            if form.is_valid():
                try:
                    mail.send_mass_mail(
                            queryset.values_list('email', flat=True),
                            **form.cleaned_data)
                except smtplib.SMTPException as e:
                    errors = unicode(e)
                return render(
                        request,
                        'admin/send_email.html',
                        {'form': form, 'errors': errors})
        if not form:
            form = self.MailForm(
                    initial={
                        'host': 'smtp.gmail.com',
                        'port': '587',
                        '_selected_action': [
                            unicode(pk)
                            for pk in queryset.values_list('id', flat=True)
                            ]
                        })

        return render(
                request,
                'admin/send_email.html',
                {'form': form, 'errors': errors})
    send_mail.short_description = _(u'send email')


class PDFFileAdmin(utils.ModelAdmin):
    """ Administration for PDF files.
    """

    list_display = (
            'id',
            'uuid',
            'base_info',
            'file_type',
            'commit_timestamp',
            )

    list_filter = (
            'file_type',
            )

    search_fields = (
            'id',
            'base_info__uuid',
            'base_info__first_name',
            'base_info__last_name',
            )

    readonly_fields = (
            'commit_timestamp',
            )


class InfoAdmin(utils.ModelAdmin):
    """ Base class for info administration.
    """

    list_display = [
            'id',
            'base_first_name',
            'base_last_name',
            'base_email',
            'pupil_registered',
            ]

    search_fields = [
            'base__id',
            'base__first_name',
            'base__last_name',
            'base__email',
            ]

    readonly_fields = (
            'commit_timestamp',
            )

    def base_first_name(self, info):
        return info.base.first_name
    base_first_name.short_description = _(u'first name')

    def base_last_name(self, info):
        return info.base.last_name
    base_last_name.short_description = _(u'last name')

    def base_email(self, info):
        return info.base.email
    base_email.short_description = _(u'email address')

    def pupil_registered(self, info):
        """ True, if pupil filled his form.
        """
        try:
            info.base.pupilinfo_set.get()
            return True
        except models.PupilInfo.DoesNotExist:
            return False
    pupil_registered.short_description = _(u'p. reg.')
    pupil_registered.boolean = True


class TeacherAdmin(InfoAdmin):
    """ Administration for TeacherInfo.
    """

    list_display = InfoAdmin.list_display + [
            'teacher_first_name',
            'teacher_last_name',
            'teacher_email',
            'phone_number',
            ]
    search_fields = InfoAdmin.search_fields + [
            'first_name',
            'last_name',
            'email',
            ]

    def teacher_first_name(self, info):
        return info.first_name
    teacher_first_name.short_description = _(u'teacher first name')

    def teacher_last_name(self, info):
        return info.last_name
    teacher_last_name.short_description = _(u'teacher last name')

    def teacher_email(self, info):
        return info.email
    teacher_email.short_description = _(u'teacher email address')


class DirectorAdmin(InfoAdmin):
    """ Administration for DirectorInfo.
    """

    list_display = InfoAdmin.list_display + [
            'director_first_name',
            'director_last_name',
            'director_email',
            'phone_number',
            ]
    search_fields = InfoAdmin.search_fields + [
            'first_name',
            'last_name',
            'email',
            ]

    def director_first_name(self, info):
        return info.first_name
    director_first_name.short_description = _(u'director first name')

    def director_last_name(self, info):
        return info.last_name
    director_last_name.short_description = _(u'director last name')

    def director_email(self, info):
        return info.email
    director_email.short_description = _(u'director email address')


class PupilInfoAdmin(InfoAdmin):
    """ Administration for PupilInfo.
    """

    list_display = InfoAdmin.list_display + [
            'phone_number',
            ]


class TestLocationAdmin(admin.ModelAdmin):
    """ Administration for test location.
    """

    list_display = (
            'address',
            'time',
            )
    search_fields = (
            'address',
            'comment',
            )


admin.site.register(models.BaseInfo, BaseInfoAdmin)
admin.site.register(models.PupilInfo, PupilInfoAdmin)
admin.site.register(models.TeacherInfo, TeacherAdmin)
#admin.site.register(models.DirectorInfo, DirectorAdmin)
admin.site.register(models.TestingLocation, TestLocationAdmin)
admin.site.register(models.RegistrationInfo, RegistrationInfoAdmin)
admin.site.register(models.PDFFile, PDFFileAdmin)
admin.site.register(models.Info)
