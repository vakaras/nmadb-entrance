#!/usr/bin/python
# -*- coding: utf-8 -*-


""" Notifications by email.
"""


from django.core import mail
from django.utils.translation import ugettext_lazy as _
from django.template.loader import get_template
from django.template import Context
from django.contrib.sites.models import Site
from django.utils.encoding import smart_str

from nmadb_entrance.config import info
from nmadb_entrance import models
from nmadb_registration.conditions import check_condition


def attach_file(email, base_info, file_type):
    """ Attached PDFFile to email.
    """
    pdf_file = models.PDFFile.objects.get(
            base_info=base_info, file_type=file_type)
    with open(pdf_file.global_path(), 'rb') as fp:
        data = fp.read()
    filename = dict((
            (u'TH', _(u'for_teacher'),),
            (u'DH', _(u'for_director'),),
            (u'TC', _(u'teacher-form'),),
            (u'DC', _(u'director-form'),),
            (u'PC', _(u'pupil-form'),),
            ))[file_type]
    email.attach(filename + u'.pdf', data)


def confirm_base_registration(base_info):
    """ Sends base registration confirmation email.
    """

    email = mail.EmailMessage(
            u'[{0} metų NMA atranka] {1.first_name} {1.last_name}'.format(
                info.year,
                base_info))

    email.body = get_template(
            'nmadb-entrance/mail/base_confirmation_email.txt').render(
            Context({
                'base_info': base_info,
                'info': info,
                'current_site': Site.objects.get_current(),
                }))

    email.from_email = info.admin_email
    email.to = [base_info.email]

    attach_file(email, base_info, u'TH')
    attach_file(email, base_info, u'DH')

    email.send()


def delay_registration(base_info):
    """ Sends email about delayed registration to pupil and notification
    to administrator.
    """

    # Send email to administrator.

    email = mail.EmailMessage((
        u'[{0} metų NMA atranka] '
        u'{1.first_name} {1.last_name} (ISM)').format(
            INFO['year'],
            base_info))

    email.body = get_template('delay_registration_email_admin.txt').render(
            Context({
                'base_info': base_info,
                'info': INFO,
                'current_site': Site.objects.get_current(),
                }))

    email.from_email = INFO['admin_email']
    email.to = [INFO['manager_email'], 'vastrauskas@gmail.com']

    with open(base_info.get_teacher_pdf_path(), 'rb') as pdf_file:
        data = pdf_file.read()
        email.attach('mokytojui.pdf', data)

    with open(base_info.get_director_pdf_path(), 'rb') as pdf_file:
        data = pdf_file.read()
        email.attach('direktoriui.pdf', data)

    email.send()

    # Send email to pupil.

    email = mail.EmailMessage(
            u'[{0} metų NMA atranka] {1.first_name} {1.last_name}'.format(
                INFO['year'],
                base_info))

    email.body = get_template('delay_registration_email_pupil.txt').render(
            Context({
                'base_info': base_info,
                'info': INFO,
                'current_site': Site.objects.get_current(),
                }))

    email.from_email = INFO['admin_email']
    email.to = [base_info.email]

    email.send()


def send_filled_pupil_form(base_info, pupil_info):
    """ Sends notification to pupil about filled PDF form.
    """

    email = mail.EmailMessage((
        u'[{0} metų NMA atranka] {1.first_name} {1.last_name}, '
        u'mokinio anketa').format(info.year, base_info))

    email.body = get_template(
            'nmadb-entrance/mail/pupil_confirmation_email.txt').render(
            Context({
                'info': info,
                'base_info': base_info,
                }))
    email.from_email = info.admin_email
    email.to = [base_info.email]

    attach_file(email, base_info, u'PC')

    email.send()


def send_filled_teacher_form(base_info, teacher_info):
    """ Sends notification to teacher about filled PDF form.
    """

    email = mail.EmailMessage((
        u'[{0} metų NMA atranka] {1.first_name} {1.last_name}, '
        u'mokytojo rekomendacija').format(info.year, base_info))

    email.body = get_template(
            'nmadb-entrance/mail/teacher_confirmation_email.txt').render(
            Context({
                'info': info,
                'base_info': base_info,
                }))
    email.from_email = info.admin_email
    email.to = [teacher_info.email]

    attach_file(email, base_info, u'TC')

    email.send()


def send_filled_director_form(base_info, director_info):
    """ Sends notification to director about filled PDF form.
    """

    email = mail.EmailMessage((
        u'[{0} metų NMA atranka] {1.first_name} {1.last_name}, '
        u'direktoriaus rekomendacija').format(info.year, base_info))

    email.body = get_template(
            'nmadb-entrance/mail/director_confirmation_email.txt').render(
            Context({
                'info': info,
                'base_info': base_info,
                }))
    email.from_email = info.admin_email
    email.to = [director_info.email]

    attach_file(email, base_info, u'DC')

    email.send()


def send_if_all(base_info):
    """ Sends information about finished registration if all forms are
    filled.
    """

    try:
        pupil_info = base_info.pupilinfo_set.get()
        teacher_info = base_info.teacherinfo_set.get()
        director_info = base_info.directorinfo_set.get()
    except (models.PupilInfo.DoesNotExist,
            models.TeacherInfo.DoesNotExist,
            models.DirectorInfo.DoesNotExist):
        return

    if check_condition(u'pupil-notify-done'):

        email = mail.EmailMessage((
            u'[{0} metų NMA atranka] '
            u'{1.first_name} {1.last_name} baigta registracija').format(
                info.year,
                base_info))

        email.body = get_template(
                'nmadb-entrance/mail/registration_finished_pupil.txt'
                ).render(
                Context({
                    'base_info': base_info,
                    'info': info,
                    'current_site': Site.objects.get_current(),
                    }))

        email.from_email = info.admin_email
        email.to = [base_info.email]

        attach_file(email, base_info, u'TC')
        attach_file(email, base_info, u'DC')
        attach_file(email, base_info, u'PC')

        email.send()

    if check_condition(u'admin-notify-done'):

        email = mail.EmailMessage((
            u'[{0} metų NMA atranka] '
            u'{1.first_name} {1.last_name} baigta registracija').format(
                info.year,
                base_info))

        email.body = get_template(
                'nmadb-entrance/mail/registration_finished_admin.txt'
                ).render(
                Context({
                    'base_info': base_info,
                    'info': info,
                    'current_site': Site.objects.get_current(),
                    }))

        email.from_email = info.admin_email
        email.to = [info.manager_email]

        attach_file(email, base_info, u'TC')
        attach_file(email, base_info, u'DC')
        attach_file(email, base_info, u'PC')

        email.send()


def send_mass_mail(
        base_set, topic, text,
        attachment1=None, attachment1_label=None,
        attachment2=None, attachment2_label=None,
        attachment3=None, attachment3_label=None,
        **backend_args):
    """ Sends emails to base set.

    .. todo::
        Add support for HTML emails (maybe with images). Urls:

        +   http://djangosnippets.org/snippets/2215/
        +   https://docs.djangoproject.com/en/dev/topics/email/
        +   http://djangosnippets.org/snippets/1710/

    """

    attachment1_data = attachment1.read() if attachment1 else None
    attachment2_data = attachment2.read() if attachment2 else None
    attachment3_data = attachment3.read() if attachment3 else None

    emails = []
    for base_info in base_set:
        email = mail.EmailMessage(topic)
        email.body = text
        email.from_email = backend_args['username']
        email.to = [base_info.email]
        if attachment1:
            email.attach(
                    smart_str(attachment1_label or u'prisegtukas1'),
                    attachment1_data)
        if attachment2:
            email.attach(
                    smart_str(attachment2_label or u'prisegtukas2'),
                    attachment2_data)
        if attachment3:
            email.attach(
                    smart_str(attachment3_label or u'prisegtukas3'),
                    attachment3_data)
        emails.append(email)

    for i in range(0, len(emails), 7):
        connection = mail.get_connection(use_tls=True, **backend_args)
        connection.send_messages(emails[i:i + 7])
