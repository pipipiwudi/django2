import  xadmin
from .models import *


class CityDictAdmin(object):
    list_display = ['name', 'desc', 'add_time']
    search_fields = ['name', 'desc']
    list_filter = ['name', 'desc', 'add_time']
    list_per_page = 9


class CourseOrgAdmin(object):
    list_display = ['name', 'desc', 'image', 'click_nums', 'fav_nums', 'address', 'city', 'add_time']
    search_fields = ['name', 'desc', 'image', 'click_nums', 'fav_nums', 'address', 'city']
    list_filter = ['name', 'desc', 'image', 'click_nums', 'fav_nums', 'address', 'city', 'add_time']
    list_per_page = 9


class TeacherAdmin(object):
    list_display = ['org', 'name', 'work_years', 'work_company', 'work_postion', 'points', 'click_nums', 'fav_nums', 'add_time']
    search_fields = ['org', 'name', 'work_years', 'work_company', 'work_postion', 'points', 'click_nums', 'fav_nums']
    list_filter = ['org', 'name', 'work_years', 'work_company', 'work_postion', 'points', 'click_nums', 'fav_nums', 'add_time']
    list_per_page = 9


xadmin.site.register(Teacher, TeacherAdmin)
xadmin.site.register(CourseOrg, CityDictAdmin)
xadmin.site.register(CityDict, CityDictAdmin)