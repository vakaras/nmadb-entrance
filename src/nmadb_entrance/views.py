import datetime

from django.db import transaction
from django.views.generic import TemplateView
from django import shortcuts
from annoying.decorators import render_to

from nmadb_registration.conditions import check_condition
from nmadb_registration import forms as registration_forms
from nmadb_entrance import models, forms, pdf, notify
from nmadb_entrance.config import info


@render_to('nmadb-entrance/index.html')
@transaction.commit_on_success
def index(request):
    """ Shows index page.
    """

    if check_condition(u'registration-ended'):
        return shortcuts.render(
                request,
                'nmadb-entrance/ended.html',
                {
                    'info': info,
                    },
                )

    form_errors = False

    if request.method == 'POST':
        form = forms.BaseInfoForm(request.POST)
        if form.is_valid():
            base_info = form.save(commit=False)
            today = datetime.date.today()
            base_info.school_year = today.year + int(today.month >= 9)
            base_info.generated_address = None
            base_info.save()

            pdf.generate_teacher_hand_form(base_info)

            if check_condition('vip', base_info=base_info):
                # TODO
                #notify.delay_registration(base_info)
                raise Exception("Not implemented.")
                return shortcuts.redirect(
                        'nmadb-entrance-delay-registration')
            else:
                notify.confirm_base_registration(base_info)
                return shortcuts.redirect('nmadb-entrance-started')
        else:
            form_errors = True
    else:
        form = forms.BaseInfoForm()

    return {
            'info': info,
            'form': form,
            'form_errors': form_errors,
            }


@render_to('nmadb-entrance/pupil-form.html')
@transaction.commit_on_success
def add_pupil_info(request, uuid):
    """ Shows form for pupil.
    """

    base_info = shortcuts.get_object_or_404(models.BaseInfo, uuid=uuid)

    try:
        base_info.pupilinfo_set.get()
    except models.PupilInfo.DoesNotExist:
        pass
    else:
        return shortcuts.render(
                request,
                'nmadb-entrance/pupil-form-filled.html',
                {
                    'base_info': base_info,
                    'info': info,
                    },
                )

    form_errors = False
    pupil_form = None
    address_form = None

    if base_info.generated_address:
        if request.method == 'POST':
            pupil_form = forms.PupilInfoForm(request.POST)
            if pupil_form.is_valid():
                pupil_info = pupil_form.save(commit=False)
                pupil_info.base = base_info
                pupil_info.save()
                pdf.generate_pupil_filled_form(base_info, pupil_info)
                notify.send_filled_pupil_form(base_info, pupil_info)
                notify.send_if_all(base_info)
                return shortcuts.redirect(
                        'nmadb-entrance-add-pupil-info', uuid)
            else:
                form_errors = True
        else:
            pupil_form = forms.PupilInfoForm()
    else:
        if request.method == 'POST':
            pupil_form = forms.PupilInfoForm(request.POST)
            address_form = registration_forms.AddressForm(request.POST)
            if pupil_form.is_valid() and address_form.is_valid():
                address = address_form.save()
                pupil_info = pupil_form.save(commit=False)
                pupil_info.home_address = address
                pupil_info.base = base_info
                pupil_info.save()
                base_info.generated_address = unicode(address)
                base_info.save()
                pdf.generate_pupil_filled_form(base_info, pupil_info)
                notify.send_filled_pupil_form(base_info, pupil_info)
                notify.send_if_all(base_info)
                return shortcuts.redirect(
                        'nmadb-entrance-add-pupil-info', uuid)
            else:
                form_errors = True
        else:
            pupil_form = forms.PupilInfoForm()
            address_form = registration_forms.AddressForm()

    return {
            'info': info,
            'pupil_form': pupil_form,
            'address_form': address_form,
            'form_errors': form_errors,
            'base_info': base_info,
            'achievements_from_year': info.year - 2,
            }


@render_to('nmadb-entrance/teacher-form.html')
@transaction.commit_on_success
def add_teacher_info(request, uuid):
    """ Shows form for teacher.
    """

    base_info = shortcuts.get_object_or_404(models.BaseInfo, uuid=uuid)

    try:
        base_info.teacherinfo_set.get()
    except models.TeacherInfo.DoesNotExist:
        pass
    else:
        return shortcuts.render(
                request,
                'nmadb-entrance/teacher-form-filled.html',
                {
                    'base_info': base_info,
                    'info': info,
                    }
                )


    form_errors = False

    if request.method == 'POST':
        form = forms.TeacherInfoForm(request.POST)
        if form.is_valid():
            teacher_info = form.save(commit=False)
            teacher_info.base = base_info
            teacher_info.save()
            pdf.generate_teacher_filled_form(base_info, teacher_info)
            notify.send_filled_teacher_form(base_info, teacher_info)
            notify.send_if_all(base_info)
            return shortcuts.redirect(
                    'nmadb-entrance-add-teacher-info', uuid)
        else:
            form_errors = True
    else:
        form = forms.TeacherInfoForm()

    return {
            'info': info,
            'form': form,
            'form_errors': form_errors,
            'base_info': base_info,
            }


@render_to('nmadb-entrance/director-form.html')
@transaction.commit_on_success
def add_director_info(request, uuid):
    """ Shows form for director.
    """

    base_info = shortcuts.get_object_or_404(models.BaseInfo, uuid=uuid)

    try:
        base_info.directorinfo_set.get()
    except models.DirectorInfo.DoesNotExist:
        pass
    else:
        return shortcuts.render(
                request,
                'nmadb-entrance/director-form-filled.html',
                {
                    'base_info': base_info,
                    'info': info,
                    }
                )

    form_errors = False

    if request.method == 'POST':
        form = forms.DirectorInfoForm(request.POST)
        if form.is_valid():
            director_info = form.save(commit=False)
            director_info.base = base_info
            director_info.save()
            pdf.generate_director_form(base_info, director_info)
            notify.send_filled_director_form(base_info, director_info)
            notify.send_if_all(base_info)
            return shortcuts.redirect(
                    'nmadb-entrance-add-director-info', uuid)
        else:
            form_errors = True
    else:
        form = forms.DirectorInfoForm()

    return {
            'info': info,
            'form': form,
            'form_errors': form_errors,
            'base_info': base_info,
            }


class DirectTemplateView(TemplateView):
    """ The class that provides an alternative to direct_to_template.

    Source: http://stackoverflow.com/a/12150035
    """
    extra_context = None
    def get_context_data(self, **kwargs):
        context = super(self.__class__, self).get_context_data(**kwargs)
        if self.extra_context is not None:
            for key, value in self.extra_context.items():
                if callable(value):
                    context[key] = value()
                else:
                    context[key] = value
        return context
