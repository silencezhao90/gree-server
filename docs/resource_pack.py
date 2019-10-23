"""
doc for button
"""

"""
@apiGroup ResourcePack
@apiVersion 1.0.0
@api {get} /resource_packs 01. 获取资源包列表
@apiName ResourcePack01
@apiParam {Number=0,1} [order=0] 顺序: 0--desc降序(新到旧), 1--asc升序
@apiParam {Number} [limit=1000] 返回数目
@apiParam {Number} [offset=0] 偏移值


@apiSuccessExample {json} Success-Example
HTTP/1.1 200 OK
{
    "code": 10000,
    "message": "success",
    "info": {},
    "list": {
        "pagination": {
            "total": 1,
            "offset": 0,
            "limit": 1000
        },
        "data": [
            {
                "id": 1,
                "name": '资源包名称',
                "file_name": '文件名',
                "size": 100,
                "url": 地址,
                "md5": md5,
                "cover_image": 封面图,
                "add_time": 1535449799,
                "update_time": 1535449799
            }
        ]
    }
}
"""

"""
@apiGroup ResourcePack
@apiVersion 1.0.0
@api {post} /upload 02. 上传
@apiName ResourcePack02
@apiParam (String) file 上传文件
@apiUse SuccessDefaultResponse
"""

"""
@apiGroup ResourcePack
@apiVersion 1.0.0
@api {delete} /resource_packs/<number:id> 03. 删除资源包
@apiName ResourcePack03
@apiParam (uri参数) id 资源包id
@apiUse SuccessDefaultResponse
"""

"""
@apiGroup ResourcePack
@apiVersion 1.0.0
@api {put} /resource_packs/<number:id> 04. 修改资源信息
@apiName ResourcePack04
@apiParam (uri参数) id 资源包id
@apiParam {String} name 名称
@apiUse SuccessDefaultResponse
"""

"""
@apiGroup ResourcePack
@apiVersion 1.0.0
@api {get} /download/<string:filename> 05. 下载资源包
@apiName ResourcePack05
@apiParam (uri参数) filename 文件名，包含后缀
@apiUse SuccessDefaultResponse
"""

"""
@apiGroup ResourcePack
@apiVersion 1.0.0
@api {get} /resource_packs/<int:id> 06. 获取资源包详情
@apiName ResourcePack06


@apiSuccessExample {json} Success-Example
HTTP/1.1 200 OK
{
    "code": 10000,
    "message": "success",
    "info": {
        "add_time": 1551964249.75833,
        "id": 5,
        "name": "WechatIMG73.jpeg",
        "file_name": "WechatIMG73.jpeg",
        "size": 0,
        "cover_image": 封面图,
        "update_time": 1551964249.758376,
        "url": "http://127.0.0.1:8041/_uploads/files/images/WechatIMG73.jpeg"
    },
    "list": {
        "data": [],
        "pagination": false
    }
}
"""