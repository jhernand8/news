from django.contrib import admin
from django.urls import path

admin.autodiscover()

import hnproj.views
import hnproj.topstoriesviews

urlpatterns = [
    # Examples:
    # url(r'^$', 'hnproj.views.newsByUser', name='home'),
    # url(r'^blog/', include('blog.urls')),

    path('admin/', admin.site.urls),
    
    path('/', hnproj.views.newsByUser),
    path('', hnproj.views.newsByUser),
    path('users', hnproj.views.users),
    path('cronAddCurrTopItems', hnproj.views.update_top_items),
    path('removeTopStories', hnproj.views.remove_top_items),
    path('topStories', hnproj.topstoriesviews.home),
]
