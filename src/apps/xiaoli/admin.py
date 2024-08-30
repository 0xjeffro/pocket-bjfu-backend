from django.contrib import admin
from .models import XiaoLi

# Register your models here.


class XiaoLiAdmin(admin.ModelAdmin):
    list_display = ['title', 'img', 'priority']


admin.site.register(XiaoLi, XiaoLiAdmin)

