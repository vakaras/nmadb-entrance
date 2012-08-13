from django.conf.urls.defaults import patterns, url
from django.views.generic.simple import direct_to_template


urlpatterns = patterns(
    'nmadb_entrance.views',

    url(r'^$', 'index', name='nmadb-entrance-index',),
    url(r'^started/$', direct_to_template,
        {'template': 'nmadb-entrance/started.html'},
        name='nmadb-entrance-started'),
    url((
        r'student/'
        r'(?P<uuid>'
        r'[a-z0-9]{8}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{12}'
        r')/$'
        ),
        'add_pupil_info', name='nmadb-entrance-add-pupil-info'),
    )
