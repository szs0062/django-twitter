from django.core import serializers
from utils.json_encoder import JSONEncoder


class DjangoModelSerializer:

    @classmethod
    def serialize(cls, instance):
        # Django 的serializers默认需要一个query set 或者 list类型的数据来进行序列化
        # 因此需要给instance加一个[] 变成list
        return serializers.serialize('json', [instance], cls=JSONEncoder)

    @classmethod
    def deserialize(cls, serialized_data):
        # 需要加 .object 来得到原始的model类型的object数据，要不然得到的数据并不是一个
        # ORM的object, 而是一个DeserializedObject的类型
        return list(serializers.deserialize('json', serialized_data))[0].object
