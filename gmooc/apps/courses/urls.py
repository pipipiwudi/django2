from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from courses import views

urlpatterns = [
    # 课程列表
    path('list', views.CoursesList.as_view(), name='course_list'),
    # 课程详情页
    path('detail/<int:course_id>/', views.CourseDetail.as_view(), name='course_detail'),
    # 课程信息页
    path('info/<int:course_id>/', views.CourseInfoView.as_view(), name='course_info'),
    # 课程评论页
    path('comment/<int:course_id>/', views.CourseCommentView.as_view(), name='course_comment'),
    # 添加评论，异步访问
    path('add_comment/', views.AddCommentView.as_view(), name='add_comment'),

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)