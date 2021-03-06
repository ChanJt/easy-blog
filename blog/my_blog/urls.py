from django.conf.urls import patterns, include, url
from . import views,feeds

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'blog.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
	url(r'^$',views.home),
	url(r'^(?P<id>\d+)/$',views.blogpost,name='blogpost'),
	url(r'^article/(?P<slug>[-\w\d]+)-(?P<id>\d+)/$',views.article,name='article'),
	url(r'^contact/$',views.contact),
	url(r'^search/$',views.search),
	url(r'^rss/$',feeds.ArticleFeed()),
)
