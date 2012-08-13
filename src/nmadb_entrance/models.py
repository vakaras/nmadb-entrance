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


class Info(models.Model):
    """ Registration information.
    """

    address = models.CharField(
            max_length=255,
            verbose_name=_(u'address'),
            )

    year = models.PositiveSmallIntegerField(
            verbose_name=_(u'year'),
            )

    forms_send_deadline = models.DateField(
            verbose_name=_(u'forms send deadline'),
            )
