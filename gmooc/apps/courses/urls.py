from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from courses import views

urlpatterns = [
    path('list', views.CoursesList.as_view(), name='course_list'),
    path('detail/<int:course_id>/', views.CourseDetail.as_view(), name='course_detail'),
    path('info/<int:course_id>/', views.CourseInfoView.as_view(), name='course_info'),
    path('comment/<int:course_id>/', views.CourseCommentView.as_view(), name='course_comment'),
    path('add_comment/', views.AddCommentView.as_view(), name='add_comment'),

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)