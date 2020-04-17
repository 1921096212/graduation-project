from django.db import models
from django.contrib.auth.models import User


# 学生表
class Contact(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=20, verbose_name='姓名')  # 姓名
    grade = models.CharField(max_length=20, verbose_name='班级')  # 班级
    score_1 = models.CharField(max_length=10, blank=True, verbose_name='成绩1')  # 成绩1
    score_2 = models.CharField(max_length=10, blank=True, verbose_name='成绩2')  # 成绩2
    score_3 = models.CharField(max_length=10, blank=True, verbose_name='成绩3')  # 成绩3
    mod_date = models.DateTimeField(auto_now=True)  # 最后修改日期。系统自动生成

    class Meta:
        db_table = 'tb_users'
        verbose_name = '学生表'

    def __str__(self):
        return "{}".format(self.user.__str__())

