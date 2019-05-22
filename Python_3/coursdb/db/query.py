from datetime import datetime

from django.db.models import Q, Count, Avg
from pytz import UTC

from db.models import User, Blog, Topic


def create():
    user1 = User(first_name='u1', last_name='u1')
    user1.save()
    user2 = User(first_name='u2', last_name='u2')
    user2.save()
    user3 = User(first_name='u3', last_name='u2')
    user3.save()

    blog1 = Blog(title='blog1', author=user1)
    blog1.save()
    blog2 = Blog(title='blog2', author=user2)
    blog2.save()

    blog1.subscribers.add(user1, user2)
    blog2.subscribers.add(user2)

    topic1 = Topic(title='topic1', blog=blog1, author=user1)
    topic1.save()
    topic2 = Topic(title='topic2_content', blog=blog1, author=user3, created=datetime.date(2017, 1, 1))
    topic2.save()

    topic2.likes.add(user1, user2, user3)


def edit_all():
    for user in User.objects.all():
        user.first_name = 'uu1'
        user.save()


def edit_u1_u2():
    for user in User.objects.filter(Q(first_name='u1') | Q(first_name='u2')):
        user.first_name = 'uu1'
        user.save()


def delete_u1():
    for user in User.objects.get(first_name='u1'):
        user.delete()


def unsubscribe_u2_from_blogs():
    for blog in Blog.objects.all():
        for user in blog.subscribers:
            if user.first_name == 'u2':
                blog.subscribers.remove(user)


def get_topic_created_grated():
    topics = Topic.objects.filter(created__gte=datetime.date(2018, 1, 1))
    return topics


def get_topic_title_ended():
    return Topic.objects.filter(title__endswith='content').distinct()


def get_user_with_limit():
    return User.objects.filter(pk__in=[1, 2])


def get_topic_count():
    return Blog.objects.annotate(topic_count=Count('topic')).order_by('topic_count')


def get_avg_topic_count():
    return Blog.objects.annotate(topic_count=Count('topic')).aggregate(Avg('topic_count'))


def get_blog_that_have_more_than_one_topic():
    return Blog.objects.annotate(topic_count=Count('topic')).filter(topic_count__gt=1)


def get_topic_by_u1():
    return Topic.objects.filter(author__name='u1')


def get_user_that_dont_have_blog():
    return User.objects.annotate(topic_count=Count('blog')).filter(topic_count__lt=1).order_by('pk')


def get_topic_that_like_all_users():
    return Topic.objects.filter(Count('likes')==len(User.objects.all())).distinct()


def get_topic_that_dont_have_like():
    return Topic.objects.filter(Count('likes') == 0)