#_*_coding:utf-8_*_
"""
用于存储全局变量及路径
"""
import os
import time



global libPath
global reportPath #报告路径
global casePath
global imgPath
global configPath
global dataPath
global curDate


# 取路径绝对路径
PATH =lambda p:os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        p)
)

'''全局变量'''
libPath = PATH(os.path.dirname(__file__)) #lib目录
# 报告目录，绝对路径
reportPath = os.path.join(
    PATH(os.path.dirname(libPath)),
    'report'
    )


# case目录，绝对路径
casePath = os.path.join(
    PATH(os.path.dirname(libPath)),
    'testCase'
)
# 存储截图目录，绝对路径
imgPath = os.path.join(
    PATH(reportPath),
    'images')

# 配置文件目录，绝对路径
configPath = os.path.join(
    PATH(os.path.dirname(libPath)),
    'config'
)

# 数据文件目录，绝对路径
dataPath = os.path.join(
    PATH(os.path.dirname(libPath)),
    'data'
)
# 配置文件，绝对路径
configFile = os.path.join(
    configPath,
    'config.yaml'
)

# 当前日期yyyy-mm-dd
curDate = time.strftime('%Y-%m-%d')




if __name__ == "__main__":
    print("lib路径:%s"%libPath)
    print("report路径:%s"%reportPath)
    print('testCase路径:{0}'.format(casePath))
    print('report/images路径:{0}'.format(imgPath))
    print('config路径:{0}'.format(configPath))
    print('data路径:{0}'.format(dataPath))

