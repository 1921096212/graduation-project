from django.contrib import admin

# Register your models here.
from apps.userper import models

# 1. 导入默认UserAdmin 作为Base Class
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User


# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
class EmployeeInline(admin.StackedInline):
    model = models.Contact
    can_delete = False
    verbose_name_plural = 'profile'


# 2. 定义一个新的用户管理
class UserAdmin(BaseUserAdmin):
    # 3. 重新定义 list_display
    list_display = ('username', 'is_superuser', 'is_staff', 'date_joined', 'is_active')
    list_editable = ['is_superuser', 'is_staff']
    inlines = (EmployeeInline,)


# 4. 注销 User
admin.site.unregister(User)
# 5. 重新注册 User
admin.site.register(User, UserAdmin)

# 注册成绩表
admin.site.register(models.Contact)
