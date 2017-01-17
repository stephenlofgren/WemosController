"""WemosController URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from rest_framework import routers
from Base.models import D1Mini, D1MiniCommand, D1MiniEvent, D1MiniReading
from Base.models import KeyStore
from WemosController.D1MiniViewSet import UserViewSet
from WemosController.D1MiniViewSet import D1MiniViewSet
from WemosController.D1MiniCommandViewSet import D1MiniCommandViewSet
from WemosController.D1MiniEventViewSet import D1MiniEventViewSet
from WemosController.D1MiniReadingViewSet import D1MiniReadingViewSet
from WemosController.D1MiniChartsViewSet import D1MiniChartsViewSet
from WemosController.X10View import X10View
from WemosController.ZWaveView import ZWaveView

from Manage.views import lights

admin.site.register(D1Mini)
admin.site.register(D1MiniCommand)
admin.site.register(D1MiniEvent)
admin.site.register(D1MiniReading)
admin.site.register(KeyStore)

urlpatterns = [
    url(r'admin/', admin.site.urls),
]

urlpatterns += [
    url(r'Manage/lights', lights),
    url(r'x10/status/$', X10View.status),
    url(r'x10/status/([0-9]{1,2})', X10View.status),
    url(r'x10/turnOn/([a-z,A-Z])/([0-9]{1,2})$', X10View.turn_on),
    url(r'x10/turnOn/([a-z,A-Z])/([0-9]{1,2})/([0-9]{1,2})$', X10View.turn_on),
    url(r'x10/turnOff/([a-z,A-Z])/([0-9]{1,2})', X10View.turn_off),
    url(r'ZWave/turnOn/([0-9,]+)$', ZWaveView.turn_on),
    url(r'ZWave/turnOn/([0-9,]+)/([0-9]{1,2})$', ZWaveView.turn_on),
    url(r'ZWave/turnOff/([0-9,]+)', ZWaveView.turn_off),
    url(r'ZWave/status/$', ZWaveView.status),
    url(r'ZWave/status/([0-9]{1,2})$', ZWaveView.status),
]


# Routers provide an easy way of automatically determining the URL conf.
ROUTER = routers.DefaultRouter()
ROUTER.register(r'users', UserViewSet)
ROUTER.register(r'D1Minis', D1MiniViewSet)
ROUTER.register(r'Commands', D1MiniCommandViewSet)
ROUTER.register(r'Events', D1MiniEventViewSet)
ROUTER.register(r'Readings', D1MiniReadingViewSet)
ROUTER.register(r'Charts', D1MiniChartsViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns += [
    url(r'^', include(ROUTER.urls)),
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework'))
]
