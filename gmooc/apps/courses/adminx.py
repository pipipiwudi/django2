import xadmin
from .models import *


class LessonInline(object):
    model = Lesson
    extra = 0


class CourseResourceInline(object):
    model = CourseResource
    extra = 0


class CourseAdmin(object):
    list_display = ['name', 'desc', 'detail', 'degree','learn_times', 'stutents', 'fav_nums', 'image','click_nums', 'add_time']
    search_fields = ['name', 'desc', 'detail', 'degree','learn_times', 'stutents', 'fav_nums', 'image','click_nums']
    list_filter = ['name', 'desc', 'detail', 'degree','learn_times', 'stutents', 'fav_nums', 'image','click_nums', 'add_time']
    list_per_page = 5
    inlines = [LessonInline, CourseResourceInline]
    style_fields = {'detail': 'ueditor'}


class LessonAdmin(object):
    list_display = ['course', 'name', 'add_time']
    search_fields =['course', 'name']
    list_filter = ['course', 'name', 'add_time']
    list_per_page = 9


class VidioAdmin(object):
    list_display = ['lesson', 'name', 'add_time']
    search_fields = ['lesson', 'name']
    list_filter = ['lesson', 'name', 'add_time']
    list_per_page = 9


class CourseResourceAdmin(object):
    list_display = ['course', 'name', 'add_time', 'download']
    search_fields =['course', 'name', 'download']
    list_filter = ['course', 'name', 'add_time', 'download']
    list_per_page = 9


xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(Vidio, VidioAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)