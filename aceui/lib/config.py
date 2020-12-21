import yaml
from aceui.lib import gl


class CONF:

    """写YAML文件内容"""
    @staticmethod
    def write(data):
        """
        写YAML文件内容
        :param path: YAML文件路径
        :param data: 写入的数据
        :return: 无
        """
        with open(gl.configFile,'wb') as fp:
            yaml.dump(data, fp)
            fp.close()

    """读取YAML文件内容"""
    @staticmethod
    def read(file):
        """
        读取YAML内容
        :return: 指定节点内容
        """
        with open(file,'rb') as fp:
            content = fp.read().decode('utf-8')
            fp.close()

        ret = yaml.load(content, Loader=yaml.FullLoader)
        return ret

# 单例模式
CONF()