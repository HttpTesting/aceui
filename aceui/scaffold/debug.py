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




if __name__=="__main__":
    cur_path = os.getcwd()

    case_path = os.path.join(cur_path, 'testCase')

    report_path = os.path.join(cur_path, 'reports')

    if not os.path.exists(report_path):
        os.makedirs(report_path)

    suite = unittest.TestSuite()

    suite.addTest(
        unittest.defaultTestLoader.discover(case_path, 'test*.py')
    )
    filePath = os.path.join(report_path, 'Report.html')  # 确定生成报告的路径
    print(filePath)

    with open(filePath, 'wb') as fp:
        runner = HTMLTESTRunnerCN.HTMLTestRunner(
            stream=fp,
            title=u'UI自动化测试报告',
            description=u'详细测试用例结果',  # 不传默认为空
            tester="天枢"  # 测试人员名字，不传默认为小强
        )

        # 运行测试用例
        runner.run(suite)

