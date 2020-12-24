"""
create:2018/10/23
by:yhleng
"""
import time
import os
import string
import random
import zipfile
import shutil
import csv
from selenium import webdriver
import yaml
from aceui.lib import gl
from aceui.lib.config import CONF


def select_Browser_WebDriver():
    """
    根据config.yaml配置文件，来选择启动的浏览器
    :return:
    """
    #读取config.yam配置文件中，浏览器配置
    bro_name = CONF.read(gl.configFile)['CONFIG']['Browser']

    #根据borName决定，启动，哪个浏览器
    if str(bro_name).strip().lower() == 'chrome':
        driver = webdriver.Chrome()
    elif str(bro_name).strip().lower() == 'firefox':
        driver = webdriver.Firefox()
    else:
        driver = webdriver.Ie()
    return driver



def write_ymal(path, data):
    """
    写YAML文件内容
    :param path: YAML文件路径
    :param data: 写入的数据
    :return: 无
    """
    with open(path, 'wb') as fp:
        yaml.dump(data, fp)


def get_yaml_field(path):
    """
    读取YAML内容
    :param path: xxxx.YAML文件所在路径
    :return: 指定节点内容
    """
    with open(path, 'rb') as fp:
        cont = fp.read()

    ret = yaml.load(cont, Loader=yaml.FullLoader)
    return ret


def get_run_flag(scenario_key, casename):
    """
    获取运行标记，来决定是否执行
    :param scenario_key:
    :return: Y 或 N
    """
    conf = CONF.read(gl.configFile)
    return conf['RUNING'][scenario_key]['Flag'][casename]['Flag']



def cook_info(func):
    """
    从配置文件获取cookies信息
    :param func: 函数名
    :return: 函数
    """
    def warpper(*args, **kwargs):
        cook1= CONF.read(gl.configFile)['CONFIG']['Cookies']['LoginCookies']
        return func(cook=cook1, *args, **kwargs)
    return warpper


def replay(func):
    """
    回放速度
    :param func: 函数名
    :return: wrapper
    """
    def wrapper(*args, **kwargs):
        func(*args, **kwargs)
        sleeptime = float(CONF.read(gl.configFile)['RUNING']['REPLAY']['Time']) / 1000
        time.sleep(sleeptime)
        return func
    return wrapper



def hight_light_conf(key):
    """
    配置元素，是否高亮显示
    :param key: config.yaml 中关键字 HightLight:1 高亮 其它忽略
    :return:
    """
    def _wrapper(func):
        def wrapper(*args, **kwargs):
            ret = None
            if CONF.read(gl.configFile)[key] == 1:
                ret = func(*args, **kwargs)
            return ret
        return wrapper
    return _wrapper



def remove_all_files(dirpath):
    """
    删除目标,目录下文件及文件夹
    :param dirpath: 目标目录
    :return: 无
    """
    if os.path.exists(dirpath):
        shutil.rmtree(dirpath)

def zip_dir(dirpath,out_fullName):
    """
    压缩指定文件夹
    :param dirpath: 目标文件夹路径
    :param outFullName: 压缩文件保存路径+xxxx.zip
    :return: 无
    """
    zip = zipfile.ZipFile(out_fullName, "w", zipfile.ZIP_DEFLATED)
    for path, dirnames, filenames in os.walk(dirpath):
        # 去掉目标跟路径，只对目标文件夹下边的文件及文件夹进行压缩
        fpath = path.replace(dirpath, '')

        for filename in filenames:
            zip.write(
                os.path.join(path, filename),
                os.path.join(fpath, filename)
            )
    zip.close()


def reply_case_fail(num=3):
    """
    测试case失败后，重新执行功能
    :param num: 失败最多可以执行次数，默认为3次
    :return: fun本身或者抛出异常
    """
    def _warpper(func):
        def warpper(*args, **kwargs):
            raise_info = None
            rnum = 0
            num = CONF.read(gl.configFile)['RUNING']['CASE']['Retry']
            for _ in range(num):
                try:
                    ret = func(*args, **kwargs)
                    if rnum > 1:
                        print('重试{}次成功'.format(rnum))
                    return ret
                except Exception as ex:
                    rnum += 1
                    raise_info = ex
            print('重试{}次,全部失败'.format(rnum))
            raise raise_info
        return warpper
    return _warpper


def get_data(file, field):
    """
    从data目录下的yaml文件读取指定字段(field)CASE数据
    :param file:yaml数据文件
    :param field: 指定字段读取
    :return: 结构数据
    """
    yaml = (str(file).endswith('.yaml'), str(file).endswith('.yam'))
    file = '{}.yaml'.format(file) if not (yaml[0] or yaml[1]) else file
        

    field = str(field).strip().upper()
    data = CONF.read(
        os.path.join(
            gl.dataPath, file
        )
    )[field]
    return data


def create_dir(path):
    """
    如果文件夹不存在，则创建
    :param path:
    :return:
    """
    folder = os.path.exists(path)
    if not folder:
        os.makedirs(path)


def genrandomstr(lenstr=5):
    """
    随机产生数据
    :param lenstr: 需要字符串的长度,
    :return: 指定长度的字符和数字组合的字符串，例如：lenstr=5，"Qamo8"
    """
    strs = "".join(random.choice(string.ascii_letters + string.digits)
                   for _ in range(lenstr)
                   )
    return strs


def rndint(min=0, max=1):
    """
    返回一个随机整数
    :param max:
    :param min:
    :return:
    """
    return random.randint(min, int(max))


def join_url(url):
    """
    读取config基本url并拼接完整
    :param url: 页面url
    :return: 完整url
    """
    base_url = CONF.read(gl.configFile)['CONFIG']['Base_Url']

    if not url.startswith('/'):
        url = "/{}".format(url)

    return "{}{}".format(base_url, url)


def autoi(strword):
    """
    将字符串类型的数字转换成int类型
    :param strword: 字符串数字，'1,989.00'
    :return: int类型 1989
    """
    if strword.count('0') != 0 or strword.count(',') != 0:
        strword = ''.join(
            strword.split('.')[0].split(',')
        )
    
    return int(strword)



def rnd_num(len=5):
    """
    返回一个随机整数
    :param max:
    :param min:
    :return:
    """
    rnd = ''
    for _ in range(len):
        rnd += str(random.randint(0, 9))

    return rnd



def createphone():
    """
    :return: 手机号
    """
    mobile_list = ['139', '138', '136', '133',
               '134', '156', '158', '155', '159'
               ]
    phone = '{}{}'.format(
        random.choice(mobile_list),
        ''.join(random.choice('0123456789') for _ in range(8))
    )

    return phone


def write_csvfile(filepath, header, data):
    """
    :param filepath:csv文件路径
    :param header:csv文件标头（表格第一行）[]
    :param data:写入数据，[{}]
    :return:无
    """
    with open(filepath, 'w', newline='') as files:
        writer = csv.DictWriter(files, header)
        writer.writeheader()
        writer.writerows(data)


def send_dding_msg(token, msg):
    '''
    推送消息到钉群
    '''
    import requests
    payload = {
        "msgtype": "text",
        "text": {
            "content": msg,
            # "mentioned_mobile_list":["13718651998"],
        }
    }
    headers = {
        'Content-Type': 'application/json'
    }
    d_url = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={}'.format(token)

    res = requests.request('POST', d_url, headers=headers, json=payload)

    return res


if __name__ == "__main__":
    # stra = genrandomstr(20)
    # print(type(stra))
    # url = join_url('/activity/create/1024')
    print(createphone())


