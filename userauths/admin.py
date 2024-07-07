from django.contrib import admin
#from .models import User, Profile

from userauths.models import User, Profile

class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'full_name', 'is_staff')


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'image', 'country', 'about', 'date')


    def get_full_name(self, obj):
        return obj.user.full_name if obj.user.full_name else obj.user.username
    get_full_name.short_description = 'Full Name'

admin.site.register(User)
admin.site.register(Profile, ProfileAdmin)

