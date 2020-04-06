from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UniversityMember, StudentProfile, FacultyProfile, TAProfile
from .forms import UniversityMemberCreationForm, UniversityMemberChangeForm

# Create Univ Member form for admin page
class UniversityMemberAdmin(UserAdmin):
    add_form = UniversityMemberCreationForm
    form = UniversityMemberChangeForm
    model = UniversityMember
    list_display = ('access_id', 'is_staff', 'is_active',)
    list_filter = ('access_id', 'is_staff', 'is_active',)

    # Fields shown for manage user
    fieldsets = (
        (None, {
          'fields': ('access_id', 'password', 'legal_name', 
          'age', 'legal_gender', 'primary_affiliation', 'image')
          }),
        ('Permissions', {
          'classes':('collapse',),
          'fields': ('is_staff', 'is_active'),
          }),
    )

    # Fields shown for create user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('access_id', 'legal_name', 'password1', 'password2',
            'age', 'legal_gender', 'primary_affiliation', 
            'is_staff', 'is_active')}
        ),
    )
    search_fields = ('access_id',)
    ordering = ('access_id',)

admin.site.register(UniversityMember, UniversityMemberAdmin)

admin.site.register(StudentProfile)
admin.site.register(FacultyProfile)
admin.site.register(TAProfile)
