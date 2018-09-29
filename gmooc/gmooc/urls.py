"""gmooc URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path,include, re_path
import xadmin
from users import views
from django.views.static import serve
from .settings import MEDIA_ROOT
# from .settings import STATIC_ROOT


urlpatterns = [
    path('admin/', xadmin.site.urls),
    path('', views.IndexView.as_view(), name='index'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('users/', include(('users.urls', 'users'), namespace='users')),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('captcha/', include('captcha.urls')),
    path('active/<str:code>', views.ActiveView.as_view(), name='active'),
    path('forget/', views.ForgetView.as_view(), name='forget'),
    path('reset/<str:code>', views.ResetView.as_view(), name='reset'),
    path('modify/', views.ModifyView.as_view(), name='modify'),
    path('org/', include(('organization.urls', 'organization'), namespace='org')),
    path('course/', include(('courses.urls', 'courses'), namespace='course')),
    path('teacher/', include(('organization.urls', 'organization'), namespace='teacher')),
    re_path(r'media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT}),
    # re_path(r'static/(?P<path>.*)$', serve, {'document_root': STATIC_ROOT}),
    # path('ueditor/', include('DjangoUeditor.urls')),
]



