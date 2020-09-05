from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Register your models here.
from .models import User, Candidate


class AccountAdmin(UserAdmin):
    list_display = ('email','registration_no','date_joined','last_login','is_admin','is_staff')#What to display as columns
    search_fields = ('email','registration_no')#what to search by
    readonly_fields = ('last_login','date_joined','registration_no')#Non-editable fields
    ordering = ['registration_no']
    filter_horizontal = ()#
    list_filter = ()#
    fieldsets = (
        (None,{'fields':('registration_no','email','is_active')}),
    )#NO IDEA WHAT IT DOES....JUST ADD FOR NOW(ERROR OTHERWISE)

class CandidateAdmin(admin.ModelAdmin):
    list_display = ('name', 'registration_no')  # What to display as columns
    search_fields = ()  # what to search by
    readonly_fields = ('votes',)  # Non-editable fields

    filter_horizontal = ()  #
    list_filter = ()  #
    fieldsets = ()  # NO IDEA WHAT IT DOES....JUST ADD FOR NOW(ERROR OTHERWISE)


admin.site.register(User,AccountAdmin)
admin.site.register(Candidate,CandidateAdmin)