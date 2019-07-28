from django.contrib import admin
from . import models


class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'mobile', 'added_on')
    search_fields = ('name', 'email', 'mobile',)
    list_filter = ('is_blocked',)
    readonly_fields = ('token', 'password',)


admin.site.register(models.User, UserAdmin)
