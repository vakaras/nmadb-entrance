from django.conf.urls.defaults import patterns, url
from django.views.generic.simple import direct_to_template


urlpatterns = patterns(
    'nmadb_entrance.views',

    url(r'^$', 'index', name='nmadb-entrance-index',),
    url(r'^started/$', direct_to_template,
        {'template': 'nmadb-entrance/started.html'},
        name='nma-entrance-started'),
    )
