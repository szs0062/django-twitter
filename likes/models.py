from accounts.services import UserService
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


# Create your models here.
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateField(auto_now_add=True)
    object_id = models.PositiveIntegerField()  # tweet_id or comment_id
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.SET_NULL,
        null=True,
    )
    # user liked content_object at created_at
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        # 这里使用unique together 也会建一个 <user, content_type, object_id>
        # 的索引。这个索引同时还可以具备查询某个 user like 了那些不同的objects的功能
        # 因此如果unique together 改成 <content_type, object_id, user>
        # 就没有这样的效果了
        unique_together = (('user', 'content_type', 'object_id'),)
        # 这个 index 的作用是可以按时间排序某个被like的content_object的所有likes
        index_together = (
            ('content_type', 'object_id', 'created_at'),
            ('user', 'content_type', 'created_at'),
        )

    def __str__(self):
        return '{} - {} liked {} {}'.format(
            self.created_at,
            self.user,
            self.content_type,
            self.object_id,
        )

    @property
    def cached_user(self):
        return UserService.get_user_through_cache(self.user_id)

