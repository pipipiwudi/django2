from django.db.models import Q
from django.shortcuts import render
from django.views.generic import View
# Create your views here.
from .models import *
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from .forms import *
from django.http import HttpResponse
from operations.models import UserFavorite
from courses.models import Course


class TeacherListView(View):
    def get(self, request):
        all_teacher = Teacher.objects.all().order_by('add_time')
        search_keyword = request.GET.get('keywords', '')
        if search_keyword:
            all_teacher = all_teacher.filter(Q(name__icontains=search_keyword) | Q(points__icontains=search_keyword))
        sort = request.GET.get('sort', '')
        if sort == 'hot':
            all_teacher = all_teacher.order_by('-click_nums')
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_teacher, 5, request=request)

        teachers = p.page(page)

        hot_teachers = all_teacher.order_by('-click_nums')[:5]
        teacher_num = all_teacher.count()
        page_type = 'teacher'

        return render(request, 'teachers-list.html', {'all_teacher': teachers,
                                                      'sort': sort,
                                                      'hot_teachers': hot_teachers,
                                                      'teacher_num': teacher_num,
                                                      'page_type': page_type})


class TeacherDetailView(View):
    def get(self, request, teacher_id):
        teacher = Teacher.objects.get(pk=teacher_id)
        teacher.click_nums += 1
        teacher.save()
        courses = Course.objects.filter(course_teacher=teacher)
        hot_teachers = Teacher.objects.all().order_by('-click_nums')[:5]
        page_type = 'teacher'

        return render(request, 'teacher-detail.html', {'teacher': teacher,
                                                       'courses': courses,
                                                       'hot_teachers': hot_teachers,
                                                       'page_type': page_type})


class AddFavView(View):
    def post(self, request):
        fav_id = request.POST.get('fav_id', '0')
        fav_type = request.POST.get('fav_type', '0')
        if not request.user.is_authenticated:
            return HttpResponse("{'status': 'fail','msg':'用户未登陆'}", content_type='application/json')
        exist_records = UserFavorite.objects.filter(user=request.user.id, fav_id=int(fav_id), fav_type=int(fav_type))
        if exist_records:
            exist_records.delete()
            if int(fav_type) == 1:
                course = Course.objects.get(pk=int(fav_id))
                course.fav_nums -= 1
                if course.fav_nums < 0:
                    course.fav_nums = 0
                course.save()
            elif int(fav_type) == 2:
                course_org = CourseOrg.objects.get(pk=int(fav_id))
                course_org.fav_nums -= 1
                if course_org.fav_nums < 0:
                    course_org.fav_nums = 0
                course_org.save()
            elif int(fav_type) == 3:
                teacher = Teacher.objects.get(pk=int(fav_id))
                teacher.fav_nums -= 1
                if teacher.fav_nums < 0:
                    teacher.fav_nums = 0
                teacher.save()
            return HttpResponse("{'status': 'fail','msg':'收藏'}", content_type='application/json')
        else:
            user_fav = UserFavorite()
            if int(fav_id) > 0 and int(fav_type) > 0:
                user_fav.fav_type = int(fav_type)
                user_fav.fav_id = int(fav_id)
                user_fav.user = request.user
                user_fav.save()
                if int(fav_type) == 1:
                    course = Course.objects.get(pk=int(fav_id))
                    course.fav_nums += 1
                    course.save()
                elif int(fav_type) == 2:
                    course_org = CourseOrg.objects.get(pk=int(fav_id))
                    course_org.fav_nums += 1
                    course_org.save()
                elif int(fav_type) == 3:
                    teacher = Teacher.objects.get(pk=int(fav_id))
                    teacher.fav_nums += 1
                    teacher.save()
                return HttpResponse("{'status': 'success','msg':'已收藏'}", content_type='application/json')

            else:
                return HttpResponse("{'status': 'fail','msg':'收藏出错'}", content_type='application/json')


class OrgCourseView(View):
    def get(self, request, org_id):
        pagename = 'course'
        org = CourseOrg.objects.get(pk=int(org_id))
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user.id, fav_id=org_id, fav_type=2):
                has_fav = True
        all_course = org.course_set.all()
        return render(request, 'org-detail-course.html', {'all_course':all_course,
                                                           'org': org,
                                                          'pagename': pagename,
                                                          'has_fav':has_fav

                                                          })


class OrgDescView(View):
    def get(self, request, org_id):
        pagename = 'desc'
        org = CourseOrg.objects.get(pk=int(org_id))
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user.id, fav_id=org_id, fav_type=2):
                has_fav = True
        all_course = org.course_set.all()
        return render(request, 'org-detail-desc.html', {
                                                          'org': org,
                                                          'pagename': pagename,
                                                          'has_fav': has_fav

                                                          })


class OrgTeacherView(View):
    def get(self, request, org_id):
        pagename = 'teacher'
        org = CourseOrg.objects.get(pk=int(org_id))
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user.id, fav_id=org_id, fav_type=2):
                has_fav = True
        all_teacher = org.teacher_set.all()
        return render(request, 'org-detail-teachers.html', {'all_teacher': all_teacher,
                                                          'org': org,
                                                          'pagename': pagename,
                                                            'has_fav': has_fav
                                                                  })


class OrgHomeView(View):
    def get(self, request, org_id):
        pagename = 'home'
        org = CourseOrg.objects.get(pk=int(org_id))
        org.click_nums += 1
        org.save()
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user.id, fav_id=org_id, fav_type=2):
                has_fav = True
        all_course = org.course_set.all()[:3]
        all_teacher = org.teacher_set.all()[:1]
        return render(request, 'org-detail-homepage.html', {'all_course':all_course,
                                                            'all_teacher':all_teacher,
                                                            'org':org,
                                                            'pagename': pagename,
                                                            'has_fav': has_fav
                                                            })


class AddAsk(View):
    def post(self, request):
        addask_form = AddAskForm(request.POST)
        if addask_form.is_valid():
            addask_form.save(commit=True)
            return HttpResponse("{'status': 'success'}", content_type='application/json')
        else:
            return HttpResponse("{'status': 'fail', 'msg':'添加出错'}", content_type='application/json')


class OrgList(View):
    def get(self, request):
        all_citys = CityDict.objects.all()
        all_orgs = CourseOrg.objects.all()
        search_keyword = request.GET.get('keywords', '')
        if search_keyword:
            all_orgs = all_orgs.filter(Q(name__icontains=search_keyword) | Q(desc__icontains=search_keyword))
        hot_orgs = all_orgs.order_by('-click_nums')[0:5]
        city_id = request.GET.get('city', '')
        if city_id:
            all_orgs = CourseOrg.objects.filter(city_id=int(city_id))
        ct = request.GET.get('ct', '')
        if ct:
            all_orgs = CourseOrg.objects.filter(category=ct)
        sort_by = request.GET.get('sort', '')
        if sort_by == 'students':
            all_orgs = all_orgs.order_by('-students')
        elif sort_by == 'course':
            all_orgs = all_orgs.order_by('-course_nums')

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_orgs, 5, request=request)

        orgs = p.page(page)
        org_nums = all_orgs.count()
        page_type = 'org'

        return render(request, 'org-list.html', {'all_citys': all_citys,
                                                 'all_orgs': orgs,
                                                 'org_nums': org_nums,
                                                 'city_id': city_id,
                                                 'ct': ct,
                                                 'hot_orgs': hot_orgs,
                                                 'sort_by': sort_by,
                                                 'page_type': page_type})
