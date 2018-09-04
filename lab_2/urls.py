from django.conf.urls import url
from django.contrib import admin
from tweets.views import Index, Profile, PostTweet, HashTagCloud, Search

admin.autodiscover()

urlpatterns = [
    url(r'^$', Index.as_view()),
    url(r'^user/(\w+)/$', Profile.as_view()),
    url(r'^admin/', admin.site.urls),
    url(r'^user/(\w+)/post/$', PostTweet.as_view()),
    url(r'^hashTag/(\w+)/$', HashTagCloud.as_view()),
    url(r'^search/$', Search.as_view()),

]
