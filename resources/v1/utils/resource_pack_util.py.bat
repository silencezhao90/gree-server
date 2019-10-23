import json
import os
import shutil

from flask_uploads import DOCUMENTS, IMAGES, AUDIO, ARCHIVES


def get_folder(file_exp):
    if file_exp in DOCUMENTS:
        folder = 'documents'
    elif file_exp in IMAGES:
        folder = 'images'
    elif file_exp in AUDIO:
        folder = 'audios'
    elif file_exp in ARCHIVES:
        folder = 'archives'
    else:
        folder = 'data'

    return folder


class ResourcePackFileHandle(object):
    """资源包文件处理"""

    def __init__(self):
        self.scene_json = ''

    def zip(self):
        """zip压缩"""
        pass

    def unzip(self):
        """解压zip"""
        pass

    def find_file(self, work_dir, target):
        """查找目录下指定文件"""
        for dir in os.listdir(work_dir):
            if dir == '__MACOSX' or dir.startswith('.'):
                continue
            if dir == target:
                print('找到了')
                # 绝对路径
                self.scene_json = work_dir + os.sep + dir
                return
            dir = work_dir + '/' + dir
            if os.path.isdir(dir):
                self.find_file(dir, target)

    def cover_image_file(self, md5):
        """解析压缩包封面图文件"""

        # 当前工作路径
        current = os.getcwd()
        # 封面图目标路径
        target_images_dir = '{}/files/images'.format(current)
        md5_dir = '{0}/files/{1}'.format(current, md5)

        self.find_file(md5_dir, 'scene.json')

        # 读取scene.json文件
        try:
            with open(self.scene_json, 'r') as f:
                config = json.load(f)

                # 获取封面图，复制封面图到指定目录
                source_image_dir = os.path.split(self.scene_json)[0] + '/' + config['scene']['info']['thumbnail']
                f.close()
        except IOError:
            # 返回默认图片
            return 'default.jpg'

        if not os.path.exists(target_images_dir):
            os.makedirs(target_images_dir)
        shutil.copy(source_image_dir, target_images_dir)

        # 图片文件名
        _, filename_exp = os.path.split(source_image_dir)

        return filename_exp