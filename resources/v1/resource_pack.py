# -*- coding:utf-8 -*-

import os

from flask import send_from_directory
from flask_restful import Resource
from flask_restful.reqparse import Argument
from werkzeug.datastructures import FileStorage

from application import upload_resource, db
from application.response import Response, ResponseError
from models.schema.resource_pack import FileInfo
from resources.v1.utils.resource_pack import ResourcePackHandle
from utils import get_params, get_file_md5
from utils.file_manage import FileHandle
from . import *


@api.resource('/resource_packs')
class ResourcePackResource(Resource):

    def get(self):
        """资源包列表"""
        (limit, order, offset, ) = get_params([
            Argument('limit', type=int, default=1000),
            Argument('order', type=int, default=0, choices=(0, 1)),
            Argument('offset', type=int, default=0),
        ])

        queryset, count = Model.ResourcePack.queryset_filter(limit, order,
                                                             offset)
        data = Model.ResourcePack.queryset_data(queryset)

        return Response(data=data,
                        pagination=True,
                        limit=limit,
                        offset=offset,
                        total=count)


@api.resource('/resource_packs/<int:id>')
class ResourcePackIdResource(Resource):

    def put(self, id):
        (name, ) = get_params([
            Argument('name', type=str, location=('json', 'values', )),
        ])

        resource_pack = Model.ResourcePack.get_by_id(id)
        update_data = {}
        if name:
            update_data['name'] = name

        if update_data:
            resource_pack.update(update_data)
            db.session.commit()

        return Response()

    def delete(self, id):
        resource_pack = Model.ResourcePack.get_by_id(id)
        db.session.delete(resource_pack.schema)
        db.session.commit()

        return Response()

    def get(self, id):
        resource_pack = Model.ResourcePack.get_by_id(id)
        return Response(info=resource_pack.get_data())


@api.resource('/upload')
class Upload(Resource):
    def post(self):
        """上传资源包"""
        (resource, ) = get_params([
            Argument('file', type=FileStorage, location=('files',),
                     required=True),
        ])
        base_path = upload_resource.config.destination
        md5 = get_file_md5(resource)
        file_exp = resource.filename
        filename, exp = os.path.splitext(file_exp)

        if not os.path.exists(os.path.join(base_path, md5)):
            # 解压到指定目录，因为要避免解压压缩包名与解压出来的根文件名不一致，需要先读取根文件名
            file_handle = FileHandle(md5, base_path)
            z_dir = file_handle.unpack_archive(resource, base_path)

            # 将根目录文件名修改为md5作为文件名
            rename_src = '{0}/{1}'.format(base_path, z_dir)
            rename_dst = '{0}/{1}'.format(base_path, md5)
            file_handle.dir_rename(rename_src, rename_dst)

            # 压缩到download_path
            file_handle.make_archive(os.path.join(base_path, md5),
                                     os.path.join(base_path, md5))
            # 转为md5命名
            md5_name = md5 + exp

            file = Model.FileInfo.new(
                name=md5_name,
                path=os.path.join(base_path, md5_name),
                size=len(resource.read()),
                md5=md5,
                exp=exp
            )
        else:
            file = FileInfo.get_by_md5(md5)

        file_handle = ResourcePackHandle(md5)
        Model.ResourcePack.new(
            name=file_handle.get_config_name() if file_handle.get_config_name() else filename,
            file_id=file.id,
            url=md5,
            cover_image=file_handle.get_cover_image(),
        )

        db.session.commit()

        return Response()


@api.resource('/download/<string:target>')
class Download(Resource):
    def get(self, target):
        """下载资源包"""
        path = upload_resource.path(target)
        if not os.path.exists(path):
            raise ResponseError(info='该资源包不存在')

        return send_from_directory(upload_resource.config.destination,
                                   target, as_attachment=True)
