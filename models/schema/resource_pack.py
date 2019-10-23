from datetime import datetime

from application import db
from utils import generate_by_sha1_random


class FileInfo(db.Model):
    __tablename__ = 'file_info'
    id = db.Column('编号', db.Integer, primary_key=True)
    name = db.Column('文件名', db.String, nullable=False)
    exp = db.Column('文件后缀', db.String)
    path = db.Column('路径', db.String)
    size = db.Column('大小', db.Integer, default=0)
    md5 = db.Column('f_md5', db.String, default='')
    add_time = db.Column('添加时间', db.DateTime, default=datetime.now())
    resource_packs = db.relationship('ResourcePack',
                                     backref=db.backref('file', lazy='joined'))

    @classmethod
    def get_by_md5(cls, md5):
        return db.session.query(FileInfo).filter_by(md5=md5).first()


class ResourcePack(db.Model):
    __tablename__ = 'resource_pack'
    id = db.Column('编号', db.Integer, primary_key=True)
    uid = db.Column('f_uid', db.String,
                    default=generate_by_sha1_random, nullable=False)
    name = db.Column('名称', db.String, nullable=False)
    url = db.Column('资源地址', db.String)
    cover_image = db.Column('封面图', db.String)
    add_time = db.Column('添加时间', db.DateTime, default=datetime.now())
    update_time = db.Column('修改时间', db.DateTime,
                            default=datetime.now(), onupdate=datetime.now())
    file_id = db.Column('f_file_id', db.Integer, db.ForeignKey(FileInfo.id))
    same_name = db.Column('同名文件', db.String, index=True)
    index = db.Column('文件下标', db.Integer, default=0)

    __mapper_args__ = {
        "order_by": add_time.desc()
    }

    def __repr__(self):
        return self.name

