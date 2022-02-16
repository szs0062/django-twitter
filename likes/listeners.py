def incr_likes_count(sender, instance, created, **kwargs):
    from comments.models import Comment
    from django.db.models import F
    from tweets.models import Tweet

    if not created:
        return

    model_class = instance.content_type.model_class()
    if model_class != Tweet:
        comment = instance.content_object
        Comment.objects.filter(id=comment.id).update(likes_count=F('likes_count') + 1)
        return

    # 不可以使用tweet.likes_count += 1; tweet.save()的方式
    # 因为这个操作不是原子操作，必须使用update语句才是原子操作
    tweet = instance.content_object
    Tweet.objects.filter(id=tweet.id).update(likes_count=F('likes_count') + 1)


def decr_likes_count(sender, instance, **kwargs):
    from comments.models import Comment
    from tweets.models import Tweet
    from django.db.models import F

    model_class = instance.content_type.model_class()
    if model_class != Tweet:
        comment = instance.content_object
        Comment.objects.filter(id=comment.id).update(likes_count=F('likes_count') - 1)
        return

    # handle tweet likes cancel
    tweet = instance.content_object
    Tweet.objects.filter(id=tweet.id).update(likes_count=F('likes_count') - 1)
