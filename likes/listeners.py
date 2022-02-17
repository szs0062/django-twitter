from utils.redis_helper import RedisHelper


def incr_likes_count(sender, instance, created, **kwargs):
    from comments.models import Comment
    from django.db.models import F
    from tweets.models import Tweet

    if not created:
        return

    model_class = instance.content_type.model_class()
    if model_class != Tweet:
        Comment.objects.filter(id=instance.object_id).update(likes_count=F('likes_count') + 1)
        comment = instance.content_object
        RedisHelper.incr_count(comment, 'likes_count')
        return

    # 不可以使用tweet.likes_count += 1; tweet.save()的方式
    # 因为这个操作不是原子操作，必须使用update语句才是原子操作
    Tweet.objects.filter(id=instance.object_id).update(likes_count=F('likes_count') + 1)
    tweet = instance.content_object
    RedisHelper.incr_count(tweet, 'likes_count')


def decr_likes_count(sender, instance, **kwargs):
    from comments.models import Comment
    from tweets.models import Tweet
    from django.db.models import F

    model_class = instance.content_type.model_class()
    if model_class != Tweet:
        Comment.objects.filter(id=instance.object_id).update(likes_count=F('likes_count') - 1)
        comment = instance.content_object
        RedisHelper.decr_count(comment, 'likes_count')
        return

    # handle tweet likes cancel
    Tweet.objects.filter(id=instance.object_id).update(likes_count=F('likes_count') - 1)
    tweet = instance.content_object
    RedisHelper.decr_count(tweet, 'likes_count')
