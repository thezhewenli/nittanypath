from django.urls import path
from .views import *
from . import views

urlpatterns = [
  path('', views.home, name='registrar-home'),
  path('my_courses/', views.my_enrollment, name='my-enrollment'),
  path('my_teachings/', views.my_teachings, name='my-teachings'),

  # course directory
  path('course_list/', CourseListView.as_view(), name='view-courses'),
  path('course_list/<int:pk>', CourseDetailView.as_view(), name='view-course-detail'),
  path('faculty_info/<str:access_id>', views.FacultyDetailView, name='view-faculty-detail'), 

  # course forum
  path('course_forum/<int:course_id>', views.course_forum_list, name='view-course-forum'), 
  path('create_post/<int:pk>', PostCreateView.as_view(), name='create-post'),
  path('create_reply/<int:pk>', ReplyCreateView.as_view(), name='create-reply'),
  path('post_detail/<int:pk>', PostDetailView.as_view(), name='view-forum-post'), 
  path('post_detail/<int:pk>/update', PostUpdateView.as_view(), name='update-forum-post'), 
  path('post_detail/<int:pk>/delete', PostDeleteView.as_view(), name='delete-forum-post'), 
  path('drop_course/<int:pk>', EnrollmentDeleteView.as_view(), name='delete-enroll-record'), 

  # course assignment
  path('course_assignment/<int:course_id>', views.course_assignment_list, name='view-course-assignment'), 
  path('assignment_detail/<int:pk>', AssignmentDetailView.as_view(), name='view-assignment-grade'), 
  path('assignment_delete/<int:pk>', AssignmentDeleteView.as_view(), name='delete-assignment'), 
  path('assignment_update/<int:pk>', AssignmentUpdateView.as_view(), name='update-assignment'),
  path('create_assignment/<int:pk>', AssignmentCreateView.as_view(), name='create-assignment'),
]
