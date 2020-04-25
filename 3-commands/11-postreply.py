import csv
from django.contrib.auth import get_user_model
from registrar.models import Post, Reply, Course

with open('scripts/PostsReplys.csv') as csv_file:
  csv_reader = csv.reader(csv_file, delimiter=',')
  for row in csv_reader:
    # Create corresponding post and reply entry
    course = Course.objects.get(course_id=float(row[4]))
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
