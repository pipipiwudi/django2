from django.db.models import Q
from django.shortcuts import render,redirect
from django.views.generic import View
# Create your views here.
from courses.models import *
from organization.models import *
from operations.models import CourseComments, UserCourse
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from utils.mixin_utils import LoginRequiredMixin


class CourseCommentView(View):
    def get(self, request, course_id):
        course = Course.objects.get(pk=course_id)
        # 根据入参id查询对应课程的评论
        all_comment = CourseComments.objects.filter(course=course)
        return render(request, 'course-comment.html', {'all_comment': all_comment,
                                                       'course': course})


class AddCommentView(View):
    def post(self, request):
        # 判断用户是否登录，返回状态由前端判断跳转页面
        if not request.user.is_authenticated:
            return HttpResponse('{"status":"fail", "msg":"用户未登录"}', content_type='application/json')
        course_id = request.POST.get("course_id", 0)
        comments = request.POST.get("comments", "")
        # 从post中获取 课程id 评论内容并保存
        if course_id > 0 and comments:
            course_comments = CourseComments()
            course = Course.objects.get(pk=int(course_id))
            course_comments.comment = comments
            course_comments.course = course
            course_comments.user = request.user
            course_comments.save()
            return HttpResponse('{"status":"success", "msg":"评论成功"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "msg":"评论失败"}', content_type='application/json')


class CourseInfoView(View):
    def get(self, request, course_id):
        course = Course.objects.get(pk=course_id)
        # 判断用户是否登录，直接重定向
        if not request.user.is_authenticated:
            return redirect('/login/')
        else:
            user_courses = UserCourse.objects.filter(user=request.user, course=course)
            if not user_courses:
                user_course = UserCourse(user=request.user, course=course)
                user_course.save()
        # 实现课程学习人数自增
        course.stutents += 1
        course.save()
        user_courses = UserCourse.objects.filter(course=course)
        # 根据课程获得用户id的列表
        user_ids = [user_course.user.id for user_course in user_courses]
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        course_ids = [user_course.course_id for user_course in user_courses]
        # 已经学习课程 根据点击数排序
        relate_courses = Course.objects.filter(id__in=course_ids).order_by('-click_nums')
        all_resourses = CourseResource.objects.filter(course=course)
        return render(request, 'course-video.html', {'course': course,
                                                     'relate_courses': relate_courses,
                                                     'all_resourses': all_resourses
                                                     })


class CourseDetail(View):
    def get(self, request, course_id):
        course = Course.objects.get(pk=course_id)
        org = course.course_org
        # 实现点击数自增
        course.click_nums += 1
        course.save()
        # 同类型课程推荐
        tag = course.tag
        if tag:
            relate_course = Course.objects.filter(tag=tag)[:1]
        else:
            relate_course = []
        # 返回给前端用于判断显示焦点
        page_type = 'course'
        return render(request, 'course-detail.html', {'course': course,
                                                      'org': org,
                                                      'relate_course': relate_course,
                                                      'page_type': page_type
                                                      })


class CoursesList(View):
    def get(self, request):
        all_course = Course.objects.all().order_by('-add_time')
        search_keyword = request.GET.get('keywords', '')
        # 搜索功能根据name desc 是否包含关键字
        if search_keyword:
            all_course = all_course.filter(Q(name__icontains=search_keyword) | Q(desc__icontains=search_keyword))
        # 页面排序选择
        sort = request.GET.get('sort', '')
        if sort == 'hot':
            all_course = all_course.order_by('-click_nums')
        elif sort == 'students':
            all_course = all_course.order_by('-stutents')

        # 实现分页功能
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        # 每页显示个数
        p = Paginator(all_course, 9, request=request)
        # 返回对应页面
        course = p.page(page)

        hot_course = all_course.order_by('-click_nums')[:3]
        page_type = 'course'
        return render(request, 'course-list.html', {'all_course': course,
                                                    'hot_course': hot_course,
                                                    'sort': sort,
                                                    'page_type': page_type
                                                    })