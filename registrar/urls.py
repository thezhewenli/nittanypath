from django.urls import path
from .views import CourseSectionListView
from . import views

urlpatterns = [
  path('', views.home, name='registrar-home'),
  path('course_list/', CourseSectionListView.as_view(), name='view-courses'),
]