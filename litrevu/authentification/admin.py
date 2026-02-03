from django.contrib import admin
from authentification.models import User

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'super_user')
    search_fields = ('username', 'email')
    list_filter = ('super_user',)

admin.site.register(User, UserAdmin)