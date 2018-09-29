from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('info/', views.UserInfoView.as_view(), name='user_info'),
    path('image/upload/', views.UploadView.as_view(), name='image_upload'),
    path('modify/pwd/', views.ModifyPwdView.as_view(), name='modify_pwd'),
    path('sendemail_code/', views.SendEmailView.as_view(), name='sendemail_code'),
    path('update_email/', views.UpdateEmailView.as_view(), name='update_email'),
    path('mycourse/', views.MyCourseView.as_view(), name='mycourse'),
    path('myfav/', views.MyFavView.as_view(), name='myfav'),
    path('myfav_org/', views.MyFavOrgView.as_view(), name='myfav_org'),
    path('myfav_teacher/', views.MyFavTeacherView.as_view(), name='myfav_teacher'),
    path('mymessage/', views.MyMessageView.as_view(), name='mymessage'),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
