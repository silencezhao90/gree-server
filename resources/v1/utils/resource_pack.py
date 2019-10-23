import json
import os
import shutil


class ResourcePackHandle(object):
    """资源包文件处理"""

    def __init__(self, md5):
        self.scene_json = ''
        self.config = ''
        self.md5 = md5

    def _info_config(self):
        # 当前工作路径
        current = os.getcwd()
        md5_dir = '{0}/files/{1}'.format(current, self.md5)

        self._find_file(md5_dir, 'info.json')

        # 读取info.json文件
        try:
            with open(self.scene_json, 'r', encoding='utf-8') as f:
                config = json.load(f)
                f.close()
        except IOError:
            return None

        return config

    def _copy(self, source_path, target_path):
        """复制文件到指定路径"""
        if not os.path.exists(target_path):
            os.makedirs(target_path)
        shutil.copy(source_path, target_path)

    def _find_file(self, work_dir, target):
        """查找目录下指定文件"""
        for dir in os.listdir(work_dir):
            if dir == '__MACOSX' or dir.startswith('.'):
                continue
            if dir == target:
                # 绝对路径
                self.scene_json = os.path.join(work_dir, dir)
                return

            dir = os.path.join(work_dir, dir)
            if os.path.isdir(dir):
                self._find_file(dir, target)

    def get_cover_image(self):
        """解析压缩包封面图文件"""

        config = self._info_config()
        # 封面图目标路径
        target_images_dir = '{0}/files/images/{1}'.format(os.getcwd(), self.md5)

        if not config:
            return 'default.jpg'
        src_image_dir = os.path.join(os.path.split(self.scene_json)[0], config['thumbnail'])

        # 将图片拷贝到图片文件夹下
        self._copy(src_image_dir, target_images_dir)

        # 图片文件名
        _, filename = os.path.split(src_image_dir)

        return filename

    def get_config_name(self):
        config = self._info_config()
        if config:
            return config['name']
        else:
            return None
