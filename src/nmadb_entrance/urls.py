from django.conf.urls import patterns, url

from nmadb_entrance.config import info
from nmadb_entrance.views import DirectTemplateView


urlpatterns = patterns(
    'nmadb_entrance.views',

    url(r'^$', 'index', name='nmadb-entrance-index',),
    url(r'^started/$',
        DirectTemplateView.as_view(
            template_name='nmadb-entrance/started.html',
            extra_context={
                'info': info,
                },
            ),
        name='nmadb-entrance-started'),
    url((
        r'student/'
        r'(?P<uuid>'
        r'[a-z0-9]{8}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{12}'
        r')/$'
        ),
        'add_pupil_info', name='nmadb-entrance-add-pupil-info'),
    url((
        r'teacher/'
        r'(?P<uuid>'
        r'[a-z0-9]{8}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{12}'
        r')/$'
        ),
        'add_teacher_info', name='nmadb-entrance-add-teacher-info'),
    url((
        r'director/'
        r'(?P<uuid>'
        r'[a-z0-9]{8}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{12}'
        r')/$'
        ),
        'add_director_info', name='nmadb-entrance-add-director-info'),
    )
