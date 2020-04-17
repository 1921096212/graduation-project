from django.db import models


# Create your models here.

# 文章表
class Course(models.Model):
    title = models.CharField(max_length=150, verbose_name='文章标题')
    p = models.CharField(max_length=150, verbose_name='p')  # 文章id
    content = models.TextField(verbose_name='文章内容')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        ordering = ['-update_time', '-id']
        db_table = 'tb_course'
        verbose_name = '文章表'

    def __str__(self):
        return self.title


# 题库表
class Exam(models.Model):
    """
    字段:
    1,逻辑删除
    2.题目内容
    3.题目选项/json的方式存储
    4.正确答案
    考核题目为单选题
    提供答案项2-4个
    """
    title = models.TextField(verbose_name='题目')
    A = models.TextField(verbose_name='选题A', default=None, blank=True)
    B = models.TextField(verbose_name='选题B', default=None, blank=True)
    C = models.TextField(verbose_name='选题C', default=None, blank=True)
    D = models.TextField(verbose_name='选题D', default=None, blank=True)
    wor = models.IntegerField(verbose_name='答案')
    level = models.IntegerField(verbose_name='难度')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    is_delete = models.BooleanField(default=False, verbose_name='逻辑删除')

    class Meta:
        ordering = ['-update_time', '-id']
        db_table = 'tb_exam'
        verbose_name = '题库表'

    def __str__(self):
        return self.title
