from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
# Create your views here.
from django.contrib.auth.backends import ModelBackend
from users.models import UserProfile,EmailVerifyRecord, Banner
from django.db.models import Q
from django.views.generic.base import View
from .forms import LoginForm, RegisterForm, ForgetForm, ResetForm, UploadForm, ModifyUserInfoForm
from utils.email_send import send_register_email
from utils.mixin_utils import LoginRequiredMixin
from django.http import HttpResponse
import json
from operations.models import UserCourse, UserFavorite, UserMessage
from courses.models import Course
from organization.models import CourseOrg, Teacher


# 重写此方法可通过多种方式登录
class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username)|Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class ResetView(View):
    def get(self, request, code):
        all_records = EmailVerifyRecord.objects.filter(code=code)
        # 判断重置链接是否有效
        if all_records:
            for record in all_records:
                email = record.email
                return render(request, 'password_reset.html', {'email': email})
        else:
            return render(request, 'activefile.html')
        return render(request, 'login.html')


class ModifyView(View):

    def post(self, request):
        reset_form = ResetForm(request.POST)
        if reset_form.is_valid():
            pwd = request.POST.get('password', '')
            pwd2 = request.POST.get('password2', '')
            email = request.POST.get('email', '')
            # 判断密码是否一致
            if pwd != pwd2:
                return render(request, 'password_reset.html', {'email': email,'msg': '密码不一致'})
            user = UserProfile.objects.get(email=email)
            # 将明文密码加密make_password
            user.password = make_password(pwd)
            user.save()
            return render(request, 'login.html')
        else:
            email = request.POST.get('email', '')
            return render(request, 'password_reset.html', {'email': email, 'reset_form': reset_form})


class ForgetView(View):

    def get(self, request):
        forget_form = ForgetForm()
        return render(request, 'forgetpwd.html', {'forget_form': forget_form})

    def post(self, request):
        forget_form = ForgetForm(request.POST)
        # 通过form检查字段合法
        if forget_form.is_valid():
            email = request.POST.get('email', '')
            send_register_email(email,'forget')
            return render(request, 'send_success.html')
        else:
            return render(request, 'forgetpwd.html', {'forget_form': forget_form})


class ActiveView(View):

    def get(self, request, code):
        # 判断激活账户链接是否有效
        all_records = EmailVerifyRecord.objects.filter(code=code)
        if all_records:
            for record in all_records:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
        else:
            return render(request, 'activefile.html')
        return render(request, 'login.html')


class RegisterView(View):

    def get(self, request):
        register_form = RegisterForm()
        return render(request, 'register.html', {'register_form': register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        # 通过form检查字段合法
        if register_form.is_valid():
            user_name = request.POST.get('email', '')
            # 判断邮箱是否已经注册
            if UserProfile.objects.filter(email=user_name):
                return render(request, 'register.html', {'register_form': register_form, 'msg': '用户已存在'})
            pass_word = request.POST.get('password', '')
            user = UserProfile()
            user.username = user_name
            user.email = user_name
            user.password = make_password(pass_word)
            # 默认激活状态为false
            user.is_active = False
            user.save()
            # 用户信息通知
            usermessage = UserMessage()
            usermessage.user = user.id
            usermessage.message = '欢迎注册'
            usermessage.save()
            send_register_email(user_name, 'register')
            return redirect('/login/')
        else:
            return render(request, 'register.html', {'register_form': register_form})


class LoginView(View):

    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get('username', '')
            pass_word = request.POST.get('password', '')
            # 判断用户是否存在，账户密码是否正确
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                # 判断用户是否激活
                if user.is_active:
                    # 进行登录
                    login(request, user)
                    return redirect('/')
                else:
                    return render(request, 'login.html', {'msg': '用户未激活'})
            else:
                return render(request, 'login.html', {'msg': '用户名或密码错误'})
        else:
            return render(request, 'login.html', {'login_form': login_form})


class UserInfoView(View):
    def get(self, request):
        page_type = 'info'

        return render(request, 'usercenter-info.html', {"page_type": page_type})

    def post(self, request):
        user_form = ModifyUserInfoForm(request.POST,instance=request.user)
        if user_form.is_valid():
            # 通过modelform直接保存
            user_form.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(user_form.errors), content_type='application/json')


class UploadView(View):
    def post(self, request):
        # 上传修改信息request.FILES
        upload_form = UploadForm(request.POST, request.FILES, instance=request.user)
        if upload_form.is_valid():
            upload_form.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail"}', content_type='application/json')


class ModifyPwdView(View):
    def post(self, request):
        modify_form = ResetForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get('password1', '')
            pwd2 = request.POST.get('password2', '')
            if pwd1 != pwd2:
                return HttpResponse('{"status":"fail","msg":"密码不一致"}', content_type='application/json')
            else:
                request.user.password = make_password(pwd1)
                request.user.save()
                return HttpResponse('{"status":"success","msg":"修改成功"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(modify_form.errors), content_type='application/json')


class SendEmailView(View):
    def get(self, request):
        email = request.GET.get('email', '')
        if UserProfile.objects.filter(email=email):
            return HttpResponse('{"email":"邮箱已存在"}', content_type='application/json')
        else:
            send_register_email(email, 'update')
            return HttpResponse('{"status":"success","msg":"修改成功"}', content_type='application/json')


class UpdateEmailView(View):
    def post(self, request):
        email = request.POST.get('email', '')
        code = request.POST.get('code', '')
        existed_record = EmailVerifyRecord.objects.filter(email=email, code=code, send_type='update')
        if existed_record:
            request.user.email = email
            request.user.save()
            return HttpResponse('{"status":"success","msg":"修改成功"}', content_type='application/json')
        else:
            return HttpResponse('{"email":"验证码出错"}', content_type='application/json')


class MyCourseView(View):
    def get(self, request):
        course = UserCourse.objects.filter(user=request.user)

        page_type = 'course'
        return render(request, 'usercenter-mycourse.html', {"page_type": page_type,
                                                            'courses': course})


class MyFavView(View):
    def get(self, request):
        courses = []
        page_type = 'fav'
        fav_type = 'course'
        userfav = UserFavorite.objects.filter(fav_type=1, user=request.user)
        for fav in userfav:
            course = Course.objects.filter(pk=fav.fav_id)
            courses.append(course)

        return render(request, 'usercenter-fav-course.html', {"page_type": page_type,
                                                              'fav_type': fav_type,
                                                              'fav_course': courses
                                                              })


class MyFavOrgView(View):
    def get(self, request):
        org_list = []
        page_type = 'fav'
        fav_type = 'org'
        userfav = UserFavorite.objects.filter(fav_type=2, user=request.user)
        for fav in userfav:
            org = CourseOrg.objects.filter(pk=fav.fav_id)
            org_list.append(org)

        return render(request, 'usercenter-fav-org.html', {"page_type": page_type,
                                                           'fav_type': fav_type,
                                                           'fav_org': org_list})


class MyFavTeacherView(View):
    def get(self, request):
        teacher_list = []
        page_type = 'fav'
        fav_type = 'teacher'
        userfav = UserFavorite.objects.filter(fav_type=3, user=request.user)
        for fav in userfav:
            teacher = Teacher.objects.filter(pk=fav.fav_id)
            teacher_list.append(teacher)
        return render(request, 'usercenter-fav-teacher.html', {"page_type": page_type,
                                                               'fav_type': fav_type,
                                                               'fav_teacher': teacher_list})


class MyMessageView(View):
    def get(self, request):
        all_message = UserMessage.objects.filter(user=request.user.id)
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_message, 5, request=request)
        message = p.page(page)
        for item in all_message:
            item.has_read = True
            item.save()
        page_type = 'message'
        return render(request, 'usercenter-message.html', {"page_type": page_type,
                                                           'messages': message})


class LogoutView(View):
    def get(self, request):
        logout(request)

        return redirect("/"
        )


class IndexView(View):
    def get(self, request):
        all_banner = Banner.objects.all().order_by('index')[:4]
        courses = Course.objects.filter(is_banner=False)[:6]
        banner_course = Course.objects.filter(is_banner=True)[:3]

        all_orgs = CourseOrg.objects.all().order_by('add_time')[:15]
        return render(request, 'index.html', {'all_banner': all_banner,
                                              'courses': courses,
                                              'banner_course': banner_course,
                                              'all_orgs': all_orgs})





