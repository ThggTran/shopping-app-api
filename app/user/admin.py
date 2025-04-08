# user/admin.py
from django.contrib import admin
from .models import User, UserProfile, Address, Role, UserRole, UserActivityLog

class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'is_active', 'is_staff', 'date_joined')
    search_fields = ('email', 'name')
    list_filter = ('is_active', 'is_staff', 'date_joined')
    ordering = ('date_joined',)
    # filter_horizontal = ('groups', 'user_permissions')
    list_editable = ('is_active', 'is_staff')

admin.site.register(User, UserAdmin)


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'gender', 'loyalty_point', 'avatar')
    search_fields = ('user__email', 'user__name')
    list_filter = ('gender',)
    # readonly_fields = ('user',) 

admin.site.register(UserProfile, UserProfileAdmin)


class AddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'address_line', 'city', 'province', 'postal_code', 'is_default')
    search_fields = ('user__email', 'address_line', 'city', 'province')
    list_filter = ('is_default', 'city', 'province')
    ordering = ('user',)

admin.site.register(Address, AddressAdmin)


class RoleAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

admin.site.register(Role, RoleAdmin)


class UserRoleAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')
    search_fields = ('user__email', 'role__name')
    list_filter = ('role',)

admin.site.register(UserRole, UserRoleAdmin)


class UserActivityLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'timestamp', 'ip_address')
    search_fields = ('user__email', 'action')
    list_filter = ('timestamp',)
    readonly_fields = ('user', 'timestamp', 'ip_address')

admin.site.register(UserActivityLog, UserActivityLogAdmin)
