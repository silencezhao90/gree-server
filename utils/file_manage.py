import hashlib
import os
import shutil
import zipfile

from werkzeug.datastructures import FileStorage


def get_file_md5(file):
    md5 = None
    if isinstance(file, FileStorage):
        md5_obj = hashlib.md5()
        md5_obj.update(file.read())
        md5 = str(md5_obj.hexdigest()).lower()
        file.seek(0)

    return md5


class FileHandle(object):
    """文件处理"""
    def __init__(self, filename, download_path=None):
        self.filename = filename
        self.download_path = download_path

    def unpack_archive(self, src_file, target_path):
        """解压到指定目录"""
        members = []
        z_dir = None  # 根文件名
        azip = zipfile.ZipFile(src_file)
        for member in azip.namelist():
            if not member.startswith('__MACOSX') and not member.startswith(
                    '.'):
                z_dir = member.split('/')[0] if z_dir is None else z_dir
                members.append(member)

        azip.extractall(target_path, members)
        return z_dir

    def make_archive(self, target_path, src_path, format='zip'):
        """压缩到指定目录"""
        if not os.path.exists(self.download_path):
            os.makedirs(self.download_path)
        return shutil.make_archive(target_path, format, src_path)

    def dir_rename(self, src_path, target_path):
        if not os.path.exists(src_path):
            raise False
        os.rename(src_path, target_path)
