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
        all_comment = CourseComments.objects.filter(course=course)
        return render(request, 'course-comment.html', {'all_comment': all_comment,
                                                       'course': course})


class AddCommentView(View):
    def post(self, request):
        if not request.user.is_authenticated:
            return HttpResponse('{"status":"fail", "msg":"用户未登录"}', content_type='application/json')
        course_id = request.POST.get("course_id", 0)
        comments = request.POST.get("comments", "")
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

        if not request.user.is_authenticated:
            return redirect('/login/')
        else:
            user_courses = UserCourse.objects.filter(user=request.user, course=course)
            if not user_courses:
                user_course = UserCourse(user=request.user, course=course)
                user_course.save()
        course.stutents += 1
        course.save()
        user_courses = UserCourse.objects.filter(course=course)
        user_ids = [user_course.user.id for user_course in user_courses]
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        course_ids = [user_course.course_id for user_course in user_courses]
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
        course.click_nums += 1
        course.save()
        tag = course.tag
        if tag:
            relate_course = Course.objects.filter(tag=tag)[:1]
        else:
            relate_course = []

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
        if search_keyword:
            all_course = all_course.filter(Q(name__icontains=search_keyword) | Q(desc__icontains=search_keyword))
        sort = request.GET.get('sort', '')
        if sort == 'hot':
            all_course = all_course.order_by('-click_nums')
        elif sort == 'students':
            all_course = all_course.order_by('-stutents')

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_course, 9, request=request)

        course = p.page(page)
        hot_course = all_course.order_by('-click_nums')[:3]
        page_type = 'course'
        return render(request, 'course-list.html', {'all_course': course,
                                                    'hot_course': hot_course,
                                                    'sort': sort,
                                                    'page_type': page_type
                                                    })