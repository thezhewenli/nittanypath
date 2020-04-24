# Using Filter for DetailView
# Source: https://www.caktusgroup.com/blog/2018/10/18/filtering-and-pagination-django/

import django_filters
from .models import Course, Section

class CourseFilter(django_filters.FilterSet):
  class Meta:
    model = Course
    fields = ['subject', 'course_number']

class SectionFilter(django_filters.FilterSet):
  class Meta:
    model = Section
    fields = ['section_num']