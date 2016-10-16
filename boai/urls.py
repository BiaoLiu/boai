"""boai URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
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
from django.contrib.auth.models import User, Group
from django.contrib import admin
from rest_framework import permissions, routers, serializers, viewsets

# from oauth2_provider.ext.rest_framework import TokenHasReadWriteScope, TokenHasScope

admin.autodiscover()


# first we define the serializers
# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#
#
# class GroupSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Group


# ViewSets define the view behavior.
# class UserViewSet(viewsets.ModelViewSet):
#     permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#
#
# class GroupViewSet(viewsets.ModelViewSet):
#     permission_classes = [permissions.IsAuthenticated, TokenHasScope]
#     required_scopes = ['groups']
#     queryset = Group.objects.all()
#     serializer_class = GroupSerializer


# Routers provide an easy way of automatically determining the URL conf
# router = routers.DefaultRouter()
# router.register(r'users', UserViewSet)
# router.register(r'groups', GroupViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browseable API.
urlpatterns = [
    # url(r'^', include(router.urls)),
    # url(r'^oauth/', include('oauth2_provider.urls', namespace='oauth2_provider')),


    url(r'^auth/', include('boai_auth.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include('webapi.urls',namespace='webapi',app_name='webapi')),
    url(r'^wechat/', include('wechat.urls', namespace='wechat',app_name='wechat')),


]
