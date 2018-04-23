"""cloud URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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
from django.conf.urls import url,include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
#APP相关
from backend import views as backend_view
from disk import views as disk_view
from django.conf.urls import url, include
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'admin_users', backend_view.AdminUserViewSet)
router.register(r'groups', backend_view.GroupViewSet)
router.register(r'users', backend_view.UserViewSet)
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^vueapi/register',backend_view.register),
    url(r'^vueapi/login',backend_view.login),
    url(r'^vueapi/list',disk_view.list),
    url(r'^vueapi/newfolder',disk_view.newfolder),
    url(r'^vueapi/enterfolder',disk_view.enterfolder),
    url(r'^vueapi/upload',disk_view.upload),
    url(r'^vueapi/download',disk_view.download),
    url(r'^vueapi/findfile',disk_view.findfile),
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
    #url(r'^$', TemplateView.as_view(template_name="index.html")),
    #url(r'^api/', include('backend.urls', namespace='api'))
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
