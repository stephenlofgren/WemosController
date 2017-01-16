"""defines urls specific to the Management project"""
from django.conf.urls import url
from Manage.LightView import LightView

@property
def urls():
    """return urlpattern array"""
    urlpatterns = [
        url(r'^/Manage/lights/$', LightView, name='lights'),
    ]
    return urlpatterns

#urlpatterns = [
#    url(r'Manage/Lights/', LightView),
#]

