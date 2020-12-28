# ########################################################
import os
import sys
# 将根目录加入sys.path中,解决命令行找不到包的问题
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.insert(0, rootPath)
# ########################################################

import unittest
import time
from aceui.lib.config import CONF
from aceui.lib import HTMLTESTRunnerCN
from aceui.lib.emailstmp import EmailClass


'''
调试的正确姿势：
1.调试指定tetCase下用例
case_module_name  = ["testActivityCreate1.py", "testActivityCreate2.py"]

2.执行testCase下所有用例
case_module_name  = []
'''

case_module_name  = ["testActivityCreate1.py"]


def debug(title='UI自动化测试报告', desc='详细测试用例结果', tester='天枢'):
    '''debug'''
    cur_path = os.getcwd()

    case_path = os.path.join(cur_path, 'testCase')

    report_path = os.path.join(cur_path, 'reports')

    if not os.path.exists(report_path):
        os.makedirs(report_path)

    suite = unittest.TestSuite()

    if case_module_name:
        for name in case_module_name:
            suite.addTest(
                unittest.defaultTestLoader.discover(case_path, name)
            )
    else:
        suite.addTest(
                unittest.defaultTestLoader.discover(case_path, 'test*.py')
        )

    filePath = os.path.join(report_path, 'Report.html')  # 确定生成报告的路径
    print(filePath)

    with open(filePath, 'wb') as fp:
        runner = HTMLTESTRunnerCN.HTMLTestRunner(
            stream=fp,
            title=title,
            description=desc,  # 不传默认为空
            tester=tester  # 测试人员名字，不传默认为小强
        )

        # 运行测试用例
        runner.run(suite)


if __name__=="__main__":
    debug(
        title='UI自动化测试报告', 
        desc='详细测试用例结果', 
        tester='天枢'
    )

