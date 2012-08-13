import datetime

from django.db import transaction
from django.views.generic.simple import direct_to_template
from django import shortcuts
from annoying.decorators import render_to

from nmadb_registration.conditions import check_condition
from nmadb_entrance import models, forms, pdf


@render_to('nmadb-entrance/index.html')
@transaction.commit_on_success
def index(request):
    """ Shows index page.
    """

    if check_condition(u'registration-ended'):
        return direct_to_template(
                request, template='nmadb-entrance/ended.html')

    form_errors = False

    if request.method == 'POST':
        form = forms.BaseInfoForm(request.POST)
        if form.is_valid():
            base_info = form.save(commit=False)
            today = datetime.date.today()
            base_info.school_year = today.year + int(today.month >= 9)
            base_info.generated_address = None
            base_info.save()

            # TODO
            #registration_info = models.RegistrationInfo()
            #registration_info.base = base_info
            #registration_info.save()

            # TODO
            pdf.generate_teacher_hand_form(base_info)
            #pdf.generate_director_form(base_info)

            if check_condition('vip', base_info=base_info):
                # TODO
                #notify.delay_registration(base_info)
                return shortcuts.redirect(
                        'nmadb-entrance-delay-registration')
            else:
                # TODO
                #notify.confirm_base_registration(base_info)
                return shortcuts.redirect('nma-entrance-started')
        else:
            form_errors = True
    else:
        form = forms.BaseInfoForm()

    return {
            'form': form,
            'form_errors': form_errors,
            }
