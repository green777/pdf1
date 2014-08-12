from django.conf.urls import patterns, url
from file2pdf import views

urlpatterns = patterns('',
    url(r'^upload', views.upload, name='upload'),
    url(r'^success', views.success, name='success'),
    url(r'^list_content', views.list_content, name='list_content'),
) 
