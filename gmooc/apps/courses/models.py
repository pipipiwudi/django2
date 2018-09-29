from datetime import datetime
# from DjangoUeditor.models import UEditorField
from django.db import models
from organization.models import CourseOrg, Teacher


class Course(models.Model):
    name = models.CharField(max_length=50, verbose_name='课程名')
    desc = models.CharField(max_length=300, verbose_name='课程描述')
    detail = models.TextField(verbose_name='课程详情')
    # detail = UEditorField(verbose_name='课程详情', width=600, height=300, imagePath='courses/ueditor/', filePath='courses/ueditor/', default='')
    degree = models.CharField(max_length=10, choices=(('cj', '初级'), ('zj', '中级'), ('gj', '高级')), verbose_name='课程难度')
    learn_times = models.IntegerField(default=0, verbose_name='学习时长')
    stutents = models.IntegerField(default=0, verbose_name='学习人数')
    fav_nums = models.IntegerField(default=0, verbose_name='收藏人数')
    image = models.ImageField(upload_to='course/%Y/%m', verbose_name='封面')
    click_nums = models.IntegerField(default=0, verbose_name='点击量')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')
    course_org = models.ForeignKey(CourseOrg, on_delete=models.CASCADE, verbose_name='机构', null=True)
    course_teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, verbose_name='授课教师', null=True)
    category = models.CharField(max_length=20, verbose_name='课程类别', default='')
    tag = models.CharField(max_length=10, verbose_name='标签', default='')
    needknow = models.CharField(max_length=300, verbose_name='课程须知', default='')
    tips = models.CharField(max_length=300, verbose_name='学习要点', default='')
    is_banner = models.BooleanField(default=False, verbose_name='是否推广')

    class Meta:
        verbose_name = '课程'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def get_learn(self):
        return self.usercourse_set.all()[:5]

    def get_course(self):
        return self.lesson_set.all()

    def get_courseresource(self):
        return self.courseresource_set.all()


class Lesson(models.Model):
    course = models.ForeignKey(Course,on_delete=models.CASCADE, verbose_name='课程')
    name = models.CharField(max_length=100, verbose_name='章节名')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '章节'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def get_video(self):
        return self.vidio_set.all()


class Vidio(models.Model):
    lesson = models.ForeignKey(Lesson,on_delete=models.CASCADE, verbose_name='章节')
    name = models.CharField(max_length=100, verbose_name='视频名')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')
    url = models.CharField(max_length=200, verbose_name='访问地址', default='')

    class Meta:
        verbose_name = '视频'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class CourseResource(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='课程')
    name = models.CharField(max_length=100, verbose_name='名称')
    download = models.FileField(max_length=100, upload_to='resource/%Y/%m', verbose_name='资源文件')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '课程资源'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name