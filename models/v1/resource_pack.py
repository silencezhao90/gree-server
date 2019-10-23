import os

from application import db
from etc.settings import STATIC_SERVER_URL
from models.v1.model_base import ModelBase
from models.schema import ResourcePack as ResourcePackSchema, FileInfo as FileInfoSchema


class ResourcePack(ModelBase):
    @classmethod
    def _get_cls_schema(cls):
        return ResourcePackSchema

    @property
    def id(self):
        return self.schema.id

    @property
    def uid(self):
        return self.schema.uid

    @uid.setter
    def uid(self, value):
        self.schema.uid = value

    @property
    def name(self):
        return self.schema.name

    @name.setter
    def name(self, value):
        self.schema.name = value

    @property
    def size(self):
        return self.schema.size

    @size.setter
    def size(self, value):
        self.schema.size = value

    @property
    def url(self):
        return self.schema.url

    @url.setter
    def url(self, value):
        self.schema.url = value

    @property
    def path(self):
        return self.schema.path

    @path.setter
    def path(self, value):
        self.schema.path = value

    @property
    def thumbnail(self):
        return self.schema.thumbnail

    @thumbnail.setter
    def thumbnail(self, value):
        self.schema.thumbnail = value

    @property
    def add_time(self):
        return self.schema.add_time

    @add_time.setter
    def add_time(self, value):
        self.schema.add_time = value

    @property
    def update_time(self):
        return self.schema.update_time

    @update_time.setter
    def update_time(self, value):
        self.schema.update_time = value

    @classmethod
    def new(cls, name, file_id, url=None, cover_image=''):
        # 如果已经存在名称
        rp = db.session.query(ResourcePackSchema).filter_by(
            same_name=name).order_by(
            ResourcePackSchema.index.desc()).first()

        rp_name = name
        index = 0
        if rp:
            index = rp.index + 1
            rp_name = '{0}_{1}'.format(name, rp.index + 1)

        resource_pack = ResourcePackSchema(
            name=rp_name,
            file_id=file_id,
            url=url,
            cover_image=cover_image,
            same_name=name,
            index=index
        )

        db.session.add(resource_pack)
        db.session.flush()
        return cls(resource_pack)

    @classmethod
    def file_is_exists(cls, upload_file_md5):
        resource_pack = db.session.query(ResourcePackSchema).filter(
            ResourcePackSchema.md5 == upload_file_md5).first()

        if resource_pack:
            return True
        return False

#    @classmethod
#    def queryset_data(cls, queryset):
#        data_array = []
#        for q in queryset:
#            data = {
#                'id': q.id,
#                'name': q.name,
#                'file_name': q.file.name.replace(q.file.exp, 'zip'),
#                'md5': q.file.md5,
#                'size': q.file.size,
#                'cover_image': STATIC_SERVER_URL + '/images/' + q.cover_image,
#                'url': STATIC_SERVER_URL + '/' + q.url,
#                'add_time': q.add_time.timestamp(),
#                'update_time': q.update_time.timestamp()
#            }
#            data_array.append(data)
#
#        return data_array
    @classmethod
    def queryset_data(cls, queryset):
        import os
        data_array = []
        for q in queryset:
            if q.cover_image == 'default.png':
                cover_image = os.path.join(STATIC_SERVER_URL, 'images',
                                           q.cover_image)
            else:
                cover_image = os.path.join(STATIC_SERVER_URL,
                                           'images/{}'.format(q.file.md5),
                                           q.cover_image)
            data = {
                'id': q.id,
                'name': q.name,
                'file_name': q.file.name,
                'md5': q.file.md5,
                'size': q.file.size,
                'cover_image': cover_image,
                'url': os.path.join(STATIC_SERVER_URL, q.url),
                'add_time': q.add_time.timestamp(),
                'update_time': q.update_time.timestamp()
            }
            data_array.append(data)

        return data_array

    @classmethod
    def queryset_filter(cls, limit, order, offset):
        queryset = db.session.query(ResourcePackSchema).offset(offset).limit(limit)
        if order == 1:
            queryset = queryset.from_self().order_by(ResourcePackSchema.add_time.asc())

        return queryset, queryset.count()

    def update(self, data):
        for k, v in data.items():
            setattr(self.schema, k, v)

        db.session.flush()
        return True

#    def get_data(self):
#        return {
#            'id': self.schema.id,
#            'name': self.schema.name,
#            'file_name': self.schema.file.name.replace(self.schema.file.exp, 'zip'),
#            'size': self.schema.file.size,
#            'cover_image': self.schema.cover_image,
#            'url': self.schema.url,
#            'add_time': self.schema.add_time.timestamp(),
#            'update_time': self.schema.update_time.timestamp()
#        }
    def get_data(self):
        if self.schema.cover_image == 'default.png':
            cover_image = os.path.join(STATIC_SERVER_URL, 'images',
                                       self.schema.cover_image)
        else:
            cover_image = os.path.join(STATIC_SERVER_URL,
                                       'images/{}'.format(self.schema.file.md5),
                                       self.schema.cover_image)
        return {
            'id': self.schema.id,
            'name': self.schema.name,
            'file_name': self.schema.file.name,
            'size': self.schema.file.size,
            'cover_image': cover_image,
            'url': os.path.join(STATIC_SERVER_URL, self.schema.url),
            'add_time': self.schema.add_time.timestamp(),
            'update_time': self.schema.update_time.timestamp()
        }


class FileInfo(ModelBase):

    @classmethod
    def _get_cls_schema(cls):
        return FileInfoSchema

    @classmethod
    def new(cls, name, path, size, md5, exp):
        file = FileInfoSchema(
            name=name,
            path=path,
            size=size,
            md5=md5,
            exp=exp
        )

        db.session.add(file)
        db.session.flush()
        return file
