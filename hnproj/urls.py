from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

import hnproj.views
import hnproj.topstoriesviews

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'hnproj.views.newsByUser', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    
    url(r'^$', 'hnproj.views.newsByUser'),
    url(r'^users$', 'hnproj.views.users'),
    url(r'^newsByUser$', 'hnproj.views.newsByUser'),
    url(r'^deleteAllUsers$', 'hnproj.views.clear_out_users'),
    url(r'^addUser$', 'hnproj.views.follow_user'),
    url(r'^cronAddCurrTopItems$', 'hnproj.views.update_top_items'),
    url(r'^removeTopStories$', 'hnproj.views.remove_top_items'),
    url(r'^topStories$', 'hnproj.topstoriesviews.home'),
)
