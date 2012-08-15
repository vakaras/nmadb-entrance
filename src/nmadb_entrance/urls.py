from django.conf.urls.defaults import patterns, url
from django.views.generic.simple import direct_to_template

from nmadb_entrance.config import info


urlpatterns = patterns(
    'nmadb_entrance.views',

    url(r'^$', 'index', name='nmadb-entrance-index',),
    url(r'^started/$', direct_to_template,
        {
            'template': 'nmadb-entrance/started.html',
            'extra_context': {
                'info': info,
                },
            },
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
