import csv
from django.contrib.auth import get_user_model
from registrar.models import Post, Reply, Course, Department

with open('../2-data_parser/9-PostsReplys.csv') as csv_file:
  csv_reader = csv.reader(csv_file, delimiter=',')
  for row in csv_reader:
    # ignore if no post for one course
    if row[0] == '':
      continue
    # Create corresponding post and reply entry
    dept = Department.objects.get(department_id = row[4])
    course = Course.objects.get(subject=dept, course_number=row[5])
    post_author = get_user_model().objects.get(access_id=row[1])
    post = Post.objects.create(course_id=course,
                              post_author=post_author,
                              post_content=row[0]
                              )
    post.save()

    reply_author = get_user_model().objects.get(access_id=row[3])
    reply = Reply.objects.create(post_id = post,
                                reply_author=reply_author,
                                reply_content=row[2]
                                )
    reply.save()
