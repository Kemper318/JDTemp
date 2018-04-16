from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views


from . import views

election_id_regex = '(?P<election_id>[0-9][0-9][0-9][0-9]\-[0-9][0-9])'
urlpatterns = [
    url('^$', views.index, name='index'),
    url(r'^login/$', auth_views.login,{'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
    url(r'^elections/$', views.get_elections, name='elections'),
    url(r'^voters/', views.get_voters, name='voters'),
    url(r'^candidates/'+election_id_regex+'/vote$', views.vote, name='vote'),
    url(r'^pollingsite/(?P<PRECINCT_ID>[0-9]+)/$', views.get_voters_for_polling_site, name='voters_for_polling_site'),
    url(r'^confirmation/'+election_id_regex+'/$', views.show_confirmation_page, name='show_confirmation'),
    url(r'^scan_qr/'+election_id_regex+'/$', views.scan_qr, name='scan_qr'),
    url(r'^check_in/', views.check_in, name='check_in'),
    url(r'^verified_voter/', views.verified_voter, name='verified_voter'),
    url(r'^submit_vote/'+election_id_regex+'/$', views.submit_vote, name='submit_vote'),
    
]