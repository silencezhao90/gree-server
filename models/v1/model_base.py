from abc import ABCMeta, abstractmethod
from datetime import datetime
from enum import Enum

from application.response import ResponseError


class ModelBase:
    __metaclass__ = ABCMeta

    @classmethod
    @abstractmethod
    def _get_cls_schema(cls):
        pass

    def __new__(cls, schema):
        if schema is None:
            return None
        else:
            return object.__new__(cls)

    def __init__(self, schema):
        self.schema = schema

    @property
    def id(self):
        return self.schema.id

    @property
    def uid(self):
        return self.schema.uid

    def refresh(self):
        self.schema = self._get_cls_schema().query.get(self.schema.id)

    def to_dict(self, include_keys=None, exclude_keys=None, depth=0, lite=False):
        """ 把用 property 装饰的属性封装到一个 dict 中再返回
         :param include_keys, list, 指定需要返回的属性, 默认为全部, 但不包含下划线开始的属性
         :param exclude_keys, list, 指定需要排除的属性, 默认为 []
         :param depth, int, 深度, object 可能含有对其它 object 的引用, object.to_dict() 调用限定两层
         :param lite, boolean, 是否为精简版, 在精简版中还会考虑 object 的 lite_exclude_keys
         """
        return_dict = {}

        attrs = self.__class__.__dict__

        include_keys = include_keys or [
            name for name in attrs.keys() if not name.startswith("_")
        ]
        exclude_keys = exclude_keys or []

        if lite is True:
            lite_exclude_keys = getattr(self, "lite_exclude_keys", [])
            exclude_keys = exclude_keys + lite_exclude_keys

        include_keys = [name for name in include_keys if name not in exclude_keys]

        if depth > 1:
            return self.uid

        for key, value in attrs.items():
            if key not in include_keys:
                continue
            if not isinstance(value, property):
                continue
            value = getattr(self, key)
            if isinstance(value, Enum):
                return_dict[key] = value.value

            elif isinstance(value, list):
                list_values = []
                for item in value:
                    if hasattr(item, "to_dict"):
                        list_values.append(item.to_dict(depth=depth + 1, lite=True))
                    else:
                        list_values.append(item)
                return_dict[key] = list_values

            elif isinstance(value, dict):
                dict_values = {}
                for k, v in value.items():
                    if hasattr(v, "to_dict"):
                        dict_values[k] = v.to_dict(depth=depth + 1, lite=True)
                    else:
                        dict_values[k] = v
                return_dict[key] = dict_values

            elif isinstance(value, datetime):
                return_dict[key] = value.isoformat()

            elif hasattr(value, "to_dict"):
                return_dict[key] = value.to_dict(depth=depth + 1, lite=True)

            else:
                return_dict[key] = value
        return return_dict

    @classmethod
    def get_by_id(cls, id):
        schema = cls._get_cls_schema().query.get(id)
        if schema is None:
            raise ResponseError(info='对应编号信息不存在')
        return cls(schema)

    @classmethod
    def get_by_uid(cls, uid):
        schema = cls._get_cls_schema().query.filter_by(uid=uid).first()
        return cls(schema)
