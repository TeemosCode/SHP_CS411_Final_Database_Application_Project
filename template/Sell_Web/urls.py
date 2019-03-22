from django.conf.urls import patterns, include, url
from Sellapp import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'Sell_Web.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    #url(r'^admin/', include(admin.site.urls)),
    url(r'images/(?P<path>.*)','django.views.static.serve',{'document_root':'./Sellapp/template/images'}),
    url(r'css/(?P<path>.*)','django.views.static.serve',{'document_root':'./Sellapp/template/css'}),
    url(r'js/(?P<path>.*)','django.views.static.serve',{'document_root':'./Sellapp/template/js'}),
    url(r'^$', views.homepage),
    url(r'^my-account/$',views.checkaccount),
    url(r'^login/$',views.login),
    url(r'^register/$',views.register),
    url(r'^editaddress/$',views.editaddress),
    url(r'^changepasswd/$',views.changepasswd),
    url(r'^mycart/$',views.checkcart),
    url(r'^shop/$',views.shop),
    url(r'^logout/$',views.logout),
    url(r'^addpro/$',views.addpro),
    url(r'^editpro/$',views.editpro),
    url(r'^modpro/([^/]+)/$',views.modpro),
    url(r'^statistics/$',views.statistics),
    url(r'^proinfo/([^/]+)/$',views.proinfo),
    url(r'^viewdetail/([^/]+)/$',views.viewdetail),
    url(r'^confirmorder/$',views.confirmorder),
    url(r'^addsuccess/([^/]+)/$',views.addsuccess),
    url(r'^get_check_code_image/$', 'get_check_code_image'),
)
