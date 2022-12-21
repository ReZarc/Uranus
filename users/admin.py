from django.contrib import admin
from django.contrib.auth.models import User
from .models import UserProfile, EmailVerifyRecord
from django.contrib.auth.admin import UserAdmin

# Register your models here.

# 取消关联注册 User
admin.site.unregister(User)  # 取消关联注册


class UserProfileInLine(admin.StackedInline):
    model = UserProfile  # 关联的模型


# 关联 UserProfile
class UserProfileAdmin(UserAdmin):
    inlines = [UserProfileInLine]


# 注册 User 模型
admin.site.register(User, UserProfileAdmin)


@admin.register(EmailVerifyRecord)
class Admin(admin.ModelAdmin):
    list_display = ('code',)
