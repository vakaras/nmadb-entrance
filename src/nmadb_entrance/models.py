import os

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core import validators

from django_db_utils import models as utils_models
from nmadb_registration import models as registration_models
from project import settings


class BaseInfo(models.Model):
    """ Info, which marks that pupil have started registration.
    """

    GENDER_CHOICES = (
            (u'M', _(u'Male')),
            (u'F', _(u'Female')),
            )

    uuid = utils_models.UUIDField(
            verbose_name=_(u'registration identifier'))

    first_name = utils_models.FirstNameField(
            verbose_name=_(u'first name'),
            )

    last_name = utils_models.LastNameField(
            verbose_name=_(u'last name'),
            )

    gender = models.CharField(
            max_length=2,
            choices=GENDER_CHOICES,
            verbose_name=_(u'gender'),
            )

    school = models.ForeignKey(
            registration_models.School,
            verbose_name=_(u'school'),
            )

    email = models.EmailField(
            max_length=128,
            verbose_name=_(u'email address'),
            )

    section = models.ForeignKey(
            registration_models.Section,
            verbose_name=_(u'section'),
            )

    school_class = models.PositiveSmallIntegerField(
            validators=[
                validators.MinValueValidator(6),
                validators.MaxValueValidator(11),
                ],
            verbose_name=_(u'class'),
            )

    school_year = models.IntegerField(
            validators=[
                validators.MinValueValidator(2005),
                validators.MaxValueValidator(2015),
                ],
            verbose_name=_(u'class update year'),
            help_text=_(
                u'This field value shows, at which year January 3 day '
                u'student was in school_class.'
                ),
            )

    generated_address = models.CharField(
            max_length = 255,
            blank=True,
            null=True,
            )

    commit_timestamp = models.DateTimeField(
            verbose_name=_(u'commit timestamp'),
            auto_now_add=True,
            )

    class Meta(object):
        ordering = [u'last_name', u'first_name']
        verbose_name = _(u'base info')
        verbose_name_plural = _(u'base infos')

    def __unicode__(self):
        return u'<{0.id}> {0.first_name} {0.last_name}'.format(self)



class PupilInfo(models.Model):
    """ Information, entered by pupil.
    """

    base = models.ForeignKey(
            BaseInfo,
            verbose_name=_(u'base info'),
            )

    home_address = models.ForeignKey(
            registration_models.Address,
            verbose_name=_(u'home address'),
            help_text=_(
                u'Null only if base_info.generated_address is present.'),
            blank=True,
            null=True,
            )

    phone_number = utils_models.PhoneNumberField(
            verbose_name=_(u'phone number'),
            )

    birth_date = models.DateField(
            verbose_name=_(u'birth date'),
            )

    # FIXME: Normalize.
    international_achievements = models.TextField(
            blank=True,
            null=True,
            verbose_name=_(u'international achievements'),
            )

    national_achievements = models.TextField(
            blank=True,
            null=True,
            verbose_name=_(u'national achievements'),
            )

    district_achievements = models.TextField(
            blank=True,
            null=True,
            verbose_name=_(u'district achievements'),
            )

    scholarschips = models.TextField(
            blank=True,
            null=True,
            verbose_name=_(u'scholarschips'),
            )

    other_achievements = models.TextField(
            blank=True,
            null=True,
            verbose_name=_(u'other achievements'),
            )

    interests = models.TextField(
            verbose_name=_(u'interests'),
            )

    motivation = models.TextField(
            verbose_name=_(u'motivation'),
            )

    future = models.TextField(
            verbose_name=_(u'future'),
            )

    come_from = models.TextField(
            verbose_name=_(u'come from'),
            )

    commit_timestamp = models.DateTimeField(
            verbose_name=_(u'commit timestamp'),
            auto_now_add=True,
            )

    class Meta(object):
        ordering = [u'base',]
        verbose_name = _(u'pupil info')
        verbose_name_plural = _(u'pupils infos')

    def __unicode__(self):
        return _(u'<{0.id}> base info: {0.base}').format(self)


class TeacherInfo(models.Model):
    """ Information, entered by teacher.
    """

    ABILITY_CHOICES = (
            (1, _(u'Excellent')),
            (2, _(u'Very good')),
            (3, _(u'Good')),
            (4, _(u'Enough')),
            (5, _(u'Satisfactory')),
            (6, _(u'Weak')),
            (7, _(u'It was not possible to evaluate')),
            )

    base = models.ForeignKey(
            BaseInfo,
            verbose_name=_(u'base info'),
            )

    first_name = utils_models.FirstNameField(
            verbose_name=_(u'first name'),
            )

    last_name = utils_models.LastNameField(
            verbose_name=_(u'last name'),
            )

    address = models.CharField(
            max_length=90,
            verbose_name=_(u'contact address'),
            )

    phone_number = utils_models.PhoneNumberField(
            verbose_name=_(u'contact phone'),
            )

    email = models.EmailField(
            max_length=128,
            verbose_name=_(u'email address'),
            )

    qualification = models.CharField(
            max_length=255,
            verbose_name=_(u'qualification'),
            blank=True,
            )

    class_master = models.BooleanField(
            verbose_name=_(u'class master'),
            blank=True,
            )

    subject_teacher = models.CharField(
            max_length=32,
            verbose_name=_('subject teacher'),
            blank=True,
            )

    other_relation = models.CharField(
            max_length=32,
            verbose_name=_('other'),
            blank=True,
            )

    years = models.PositiveSmallIntegerField(
            verbose_name=_(u'know years'),
            )

    social = models.BooleanField(
            verbose_name=_(u'socially supported'),
            )

    systemic_thinking_ability = models.IntegerField(
            choices=ABILITY_CHOICES,
            verbose_name=_(u'systemic thinking ability'),
            )

    analytical_thinking_ability = models.IntegerField(
            choices=ABILITY_CHOICES,
            verbose_name=_(u'analytical thinking ability'),
            )

    deductive_thinking_ability = models.IntegerField(
            choices=ABILITY_CHOICES,
            verbose_name=_(u'deductive thinking ability'),
            )

    self_studying_ability = models.IntegerField(
            choices=ABILITY_CHOICES,
            verbose_name=_(u'self studying ability'),
            )

    team_working_ability = models.IntegerField(
            choices=ABILITY_CHOICES,
            verbose_name=_(u'team working ability'),
            )

    oral_expression_ability = models.IntegerField(
            choices=ABILITY_CHOICES,
            verbose_name=_(u'oral expression ability'),
            )

    written_expression_ability = models.IntegerField(
            choices=ABILITY_CHOICES,
            verbose_name=_(u'written expression ability'),
            )

    receptivity_ability = models.IntegerField(
            choices=ABILITY_CHOICES,
            verbose_name=_(u'receptivity ability'),
            )

    comment = models.TextField(
            verbose_name=_(u'comment'),
            )

    commit_timestamp = models.DateTimeField(
            verbose_name=_(u'commit timestamp'),
            auto_now_add=True,
            )

    class Meta(object):
        ordering = [u'base',]
        verbose_name = _(u'teacher form')
        verbose_name_plural = _(u'teachers forms')

    def __unicode__(self):
        return _(u'<{0.id}> base info: {0.base}').format(self)


class DirectorInfo(models.Model):
    """ Information, entered by director.
    """

    base = models.ForeignKey(
            BaseInfo,
            verbose_name=_(u'base info'),
            )

    first_name = utils_models.FirstNameField(
            verbose_name=_(u'first name'),
            )

    last_name = utils_models.LastNameField(
            verbose_name=_(u'last name'),
            )

    address = models.CharField(
            max_length=90,
            verbose_name=_(u'contact address'),
            )

    phone_number = utils_models.PhoneNumberField(
            verbose_name=_(u'contact phone'),
            )

    email = models.EmailField(
            max_length=128,
            verbose_name=_(u'email address'),
            )

    study_years = models.PositiveSmallIntegerField(
            verbose_name=_(u'pupil study in school years'),
            )

    social = models.BooleanField(
            verbose_name=_(u'socially supported'),
            )

    comment = models.TextField(
            verbose_name=_(u'comment'),
            )

    commit_timestamp = models.DateTimeField(
            verbose_name=_(u'commit timestamp'),
            auto_now_add=True,
            )

    class Meta(object):
        ordering = [u'base',]
        verbose_name = _(u'director form')
        verbose_name_plural = _(u'directors forms')

    def __unicode__(self):
        return _(u'<{0.id}> base info: {0.base}').format(self)


class TestingLocation(models.Model):
    """ Information about location, where students will take tests.
    """

    address = models.CharField(
            max_length=90,
            verbose_name=_(u'address'),
            )

    time = models.DateTimeField(
            verbose_name=_(u'time'),
            )

    comment = models.TextField(
            verbose_name=_(u'comment'),
            blank=True,
            )

    class Meta(object):
        ordering = [u'time',]
        verbose_name = _(u'testing location')
        verbose_name_plural = _(u'testing locations')

    def __unicode__(self):
        return u'{0.address} {0.time}'.format(self)


class RegistrationInfo(BaseInfo):
    """ Information about state in registration process.
    """

    payed = models.BooleanField(
            verbose_name=_(u'payed'),
            blank=True,
            help_text=_(u'True, if pupil have payed registration fee.'),
            )

    pupil_form_received = models.BooleanField(
            verbose_name=_(u'pupil received'),
            help_text=_(u'True, if pupil form was received.'),
            blank=True,
            )

    teacher_form_received = models.BooleanField(
            verbose_name=_(u'teacher received'),
            help_text=_(u'True, if teacher form was received.'),
            blank=True,
            )

    director_form_received = models.BooleanField(
            verbose_name=_(u'director received'),
            help_text=_(u'True, if director form was received.'),
            blank=True,
            )

    marks_form_received  = models.BooleanField(
            verbose_name=_(u'marks received'),
            help_text=_(u'True, if pupil marks form were received.'),
            blank=True,
            )

    comment = models.TextField(
            verbose_name=_(u'comment'),
            blank=True,
            )

    done  = models.BooleanField(
            verbose_name=_(u'done'),
            blank=True,
            )

    testing_location = models.ForeignKey(
            TestingLocation,
            related_name='registration_info',
            verbose_name=_(u'Testing location'),
            blank=True,
            null=True,
            )

    socialy_supported = models.NullBooleanField(
            verbose_name=_(u'socially supported'),
            )

    class Meta(object):
        verbose_name = _(u'Registration info')
        verbose_name_plural = _(u'Registration infos')

    def __unicode__(self):
        return u'<{0.id}> {0.first_name} {0.last_name}'.format(self)


class PDFFile(models.Model):
    """ Forms filled and unfilled as PDF files.
    """

    FILE_TYPES = (
            (u'TH', _(u'teacher form filled by hand'),),
            (u'DH', _(u'director form filled by hand'),),
            (u'TC', _(u'teacher form filled with computer'),),
            (u'DC', _(u'director form filled with computer'),),
            (u'PC', _(u'pupil form filled with computer'),),
            )

    uuid = utils_models.UUIDField(
            verbose_name=_(u'file identifier'),
            )

    base_info = models.ForeignKey(
            BaseInfo,
            verbose_name=_(u'base info'),
            )

    file_type = models.CharField(
            max_length=3,
            choices=FILE_TYPES,
            verbose_name=_(u'type'),
            )

    commit_timestamp = models.DateTimeField(
            verbose_name=_(u'commit timestamp'),
            auto_now_add=True,
            )

    @property
    def path(self):
        """ Returns path to saved file.
        """
        return os.path.join('nmadb', 'entrance', self.uuid)

    def global_path(self):
        """ Returns global path to saved file.
        """
        return os.path.join(settings.MEDIA_ROOT, self.path)

    def get_absolute_url(self):
        """ Returns download link to file.
        """
        return settings.MEDIA_URL + self.path

    class Meta(object):
        verbose_name = _(u'PDF file')
        verbose_name_plural = _(u'PDF files')
        unique_together = (('base_info', 'file_type'),)


class Info(models.Model):
    """ Registration information.
    """

    address = models.CharField(
            max_length=255,
            verbose_name=_(u'address'),
            )

    address_multiline = models.TextField(
            verbose_name=_(u'address multiline'),
            )

    year = models.PositiveSmallIntegerField(
            verbose_name=_(u'year'),
            )

    forms_send_deadline = models.DateField(
            verbose_name=_(u'forms send deadline'),
            )

    manager_name_dative = models.CharField(
            max_length=128,
            verbose_name=_(u'manager name dative'),
            )

    manager_email = models.EmailField(
            verbose_name=_(u'manager email'),
            )

    manager_phone = utils_models.PhoneNumberField(
            verbose_name=_(u'manager phone'),
            )

    admin_email = models.EmailField(
            verbose_name=_(u'administrator email'),
            )

    pupil_form_deadline = models.DateField(
            verbose_name=_(u'pupil form deadline'),
            )

    entrance_fee = models.PositiveSmallIntegerField(
            verbose_name=_(u'entrance fee'),
            )

    firm_title = models.CharField(
            max_length=255,
            verbose_name=_(u'firm title'),
            )

    firm_code = models.CharField(
            max_length=255,
            verbose_name=_(u'firm code'),
            )

    bank_account = models.CharField(
            max_length=255,
            verbose_name=_(u'bank account'),
            )

    success_notification_deadline = models.DateField(
            verbose_name=_(u'success notification deadline'),
            )

    class Meta(object):
        verbose_name = _(u'registration system information')
        verbose_name_plural = _(u'registration system informations')
