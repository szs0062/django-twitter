from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    # One2One field 会创建一个unique index, 确保不会有多个UserProfile 指向同一个User
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    # Django还有一个ImageField, 但是尽量不要用，会有很多的其他问题，用FileField可以起到
    # 同样的效果，因为最后我们都是以文件形式存储起来，使用的是文件的URL进行访问
    avatar = models.FileField(null=True)
    # 当一个user被创建之后，会创建一个user profile的object
    # 此时用户还没来及去设置Nickname等信息，因此设置null=True
    nickname = models.CharField(null=True, max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{} {}'.format(self.user, self.nickname)


# 定义一个profile的property方法，植入到User这个model里
# 这样当我们通过user的一个实例化对象访问profile的时候，即user_instance.profile
# 就会在UserProfile中进行get_or_create来获取对应的profile的object
# 这种写法实际上是利用Python的灵活性进行hack的方法，这样会方便我们通过user快速
# 访问到对应的profile信息
def get_profile(user):
    if hasattr(user, '_cached_user_profile'):
        return getattr(user, '_cached_user_profile')
    profile, _ = UserProfile.objects.get_or_create(user=user)
    # 使用user对象的属性进行缓存（cache）， 避免多次调用用一个user的profile时
    # 重复的对数据库进行查询
    setattr(user, '_cached_user_profile', profile)
    return profile


# 给User Model 增加一个profile的property方法用于快捷访问
User.profile = property(get_profile)

