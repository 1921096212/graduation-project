from django.contrib import admin
from . import models

admin.site.site_header = '后台管理系统'


# Register your models here.
@admin.register(models.Course)
class CourseAdmin(admin.ModelAdmin):
    name = '111'
    # 要在admin界面显示的字段
    list_display = ['id', 'title', 'p']
    # list_per_page设置每页显示多少条记录，默认是100条
    # list_per_page = 30
    # ordering设置默认排序字段，负号表示降序排序
    ordering = ('-id',)
    # 设置哪些字段可以点击进入编辑界面
    list_display_links = ('title',)
    # list_editable 设置默认可编辑字段
    # list_editable = ['title']
    # fk_fields 设置显示外键字段
    # fk_fields = ('content',)


@admin.register(models.Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'wor', 'level']
    list_editable = ['wor', 'level']
    list_filter = ('level',)  # 过滤器
    list_display_links = ('title',)
