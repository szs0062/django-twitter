class HBaseField:
    field_type = None

    def __init__(self, reverse=False, column_family=None):
        self.reverse = reverse
        self.column_family = column_family
        # <HOMEWOKR>
        # 增加is_required属性，默认为true和default属性，默认None
        # 并在HbaseModel中做相应的处理，抛出相应的异常信息


class IntegerField(HBaseField):
    field_type = 'int'

    def __init__(self, *args, **kwargs):
        super(IntegerField, self).__init__(*args, **kwargs)


class TimestampField(HBaseField):
    field_type = 'timestamp'

    def __init__(self, *args, **kwargs):
        super(TimestampField, self).__init__(*args, **kwargs)
