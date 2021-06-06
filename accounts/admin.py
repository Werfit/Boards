from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import *


class ReaderInline(admin.StackedInline):
    model = Reader
    can_delete = False
    verbose_name_plural = 'ReaderProfile'
    fk_name = 'user'


class BloggerInline(admin.StackedInline):
    model = Blogger
    can_delete = False
    verbose_name_plural = 'BloggerProfile'
    fk_name = 'user'


class CustomUserAdmin(UserAdmin):
    inlines = (ReaderInline, BloggerInline)

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return []

        if obj.is_blogger:
            self.inlines = (BloggerInline,)
        else:
            self.inlines = (ReaderInline,)

        return super().get_inline_instances(request, obj)


admin.site.register(User, CustomUserAdmin)
