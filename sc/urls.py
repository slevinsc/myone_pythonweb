from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
admin.autodiscover()
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'sc.views.home', name='home'),
    # url(r'^sc/', include('sc.foo.urls')),
      (r'^admin/', include(admin.site.urls)),
    # Uncomment the admin/doc line below to enable admin documentation:
      url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
      url(r'^$','example.views.current_datetime'),
      url(r'^select/$','example.views.jiujie'),
    #  url(r'^login/$','example.views.login1'),
      url(r'^action1/$','example.views.action1'),
      url(r'^test/$','example.views.test'),
      url(r'^logout/$','example.views.logout'),
      url(r'^thanks/$','example.views.thanks'),
    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
