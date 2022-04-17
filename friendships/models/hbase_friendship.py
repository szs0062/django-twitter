from django_hbase import models


class HBaseFollowing(models.HBaseModel):
    """
    存储了from_user_id follow了哪些人，row_key 按照 from_user_id + created_at 排序
    可以支持查询：
    -  A 关注的所有人按照关注时间排序
    -  A 在某个时间段内关注的人哪些
    - A 在某个时间点之后/之前关注的前X个人是谁
    """
    # row key
    from_user_id = models.IntegerField(reverse=True)
    created_at = models.TimestampField()
    # column key
    to_user_id = models.IntegerField(column_family='cf')

    class Meta:
        table_name = 'twitter_followings'
        row_key = ('from_user_id', 'created_at')


class HBaseFollower(models.HBaseModel):
    """
    存储to_user_id被哪些人follow了，row_key按照to_user_id + created_at 排序
    可以支持查询：
    - A的所有粉丝按照关注时间排序
    - A的某个时间段内被哪些粉丝关注了
    - 哪X人在某个时间点之后/之前关注了A
    """
    # row_key
    to_user_id = models.IntegerField(reverse=True)
    created_at = models.TimestampField()
    # column key
    from_user_id = models.IntegerField(column_family='cf')

    class Meta:
        row_key = ('to_user_id', 'created_at')
        table_name = 'twitter_followers'
