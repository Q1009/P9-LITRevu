from django.contrib import admin
from authentication.models import User

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email', 'is_staff')
    search_fields = ('username', 'email', 'first_name', 'last_name')
# Register your models here.
admin.site.register(User, UserAdmin)