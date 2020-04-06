from django.contrib import admin
from .models import *

admin.site.register(Department)
admin.site.register(Course)
admin.site.register(Section)
admin.site.register(Assignment)
admin.site.register(AssignmentGrade)
admin.site.register(FacultyTeachTeam)
admin.site.register(EnrollRecord)
admin.site.register(Post)
admin.site.register(Reply)