import sys
import os
import time
import shutil
import unittest
import argparse
from aceui.lib.emailstmp import EmailClass
from aceui.lib.config import CONF
from aceui.lib import (HTMLTESTRunnerCN, gl, core)
from aceui.lib.core import send_dding_msg
from aceui import __version__


def run_min():
    """
    Perfrom interface test entry.

    Args: None
    Usage:
        Command line execution.
    Return:
        There is no return.
    """

    # Takes the current path of the command line
    cur_dir = os.getcwd()
    os.chdir(cur_dir)

    parse = argparse.ArgumentParser(
        description='AceUI UI自动化测试框架',
        prog='AceUI'
    )
    parse.add_argument(
        "-v",
        "--version",
        action='version',
        version="%(prog)s {}".format(__version__),
        help='Framework version.'
    )
    parse.add_argument(
        "-f",
        "--file",
        nargs='+',
        default='',
        help='The file path; File absolute or relative path.'
    )
    parse.add_argument(
        "-d",
        "--dir",
        default='',
        help='The folder path; folder absolute or relative path.'
    )

    parse.add_argument(
        "-create",
        "--scaffold",
        nargs="+",
        default='',
        help='Build scaffoldin.'
    )
    parse.add_argument(
        "-conf",
        "--config",
        nargs="+",
        default='',
        help='Basic setting of framework.'
    )
    
    # Command line arguments are assigned to varibales.
    args = parse.parse_args()
    files = args.file
    dirs = args.dir
    scaffold = args.scaffold
    conf = args.config

    # 执行单个文件或指定目录执行
    if conf:
        if str(conf[0]).strip() == 'set':
            os.system(gl.configFile)
    elif scaffold:
        scd = os.path.join(cur_dir, str(scaffold[0]).strip())

        core.remove_all_files(scd)

        try:
            shutil.copytree(gl.scaffold_path, scd)
            print('脚手架生成完成:{}'.format(scd))
        except:
            pass
            

    if files:
        run(files, cur_dir)
    elif dirs:
        casedir = os.path.join(os.getcwd(), dirs)

        # ########################################################
        # 将根目录加入sys.path中,解决命令行找不到包的问题
        sys.path.insert(0, cur_dir)
        # ########################################################
        run(casedir, cur_dir)


def run(args, curdir):
    '''
    执行测试
    '''
    # core.remove_all_files(gl.imgPath)
    suite = unittest.TestSuite()

    if isinstance(args, list):
        for i in args:
            suite.addTest(
                unittest.defaultTestLoader.discover(curdir, pattern=i.split('\\')[1])
            )            
    else:
        suite.addTest(
            unittest.defaultTestLoader.discover(args, pattern='test*.py')
        )

    report_path = os.path.join(curdir, 'reports')
    if not os.path.exists(report_path):
        os.makedirs(report_path)

    filePath = os.path.join(report_path, 'Report.html')  # 确定生成报告的路径
    print(
        '测试报告生成路径:{}'.format(filePath)
    )

    # 配置文件
    conf = CONF.read(gl.configFile)

    with open(filePath, 'wb') as fp:
        runner = HTMLTESTRunnerCN.HTMLTestRunner(
            stream=fp,
            title= conf['REPORT']['title'],
            description= conf['REPORT']['description'],  # 不传默认为空
            tester= conf['REPORT']['tester']  # 测试人员名字，不传默认为小强
        )

        if conf['MESSAGE']['DING']:

            TMPL_MSG = '{}:★开始{}★'.format(
                time.strftime(r'%Y%m%d_%H%M%S', time.localtime(time.time())),
                conf['REPORT']['title']
            )
            send_dding_msg(conf['MESSAGE']['TOKEN'], TMPL_MSG)

        # 运行测试用例
        runner.run(suite)

        if conf['MESSAGE']['DING']:
            # TMPL_MSG = '''Pro商家后台UI自动化测试执行【已完成】:\n{}\n测试报告:http://60.205.217.8:5004/pos/pro_manage_web/report'''.format(runner.RESULT)
            TMPL_MSG = conf['MESSAGE']['MSG'].format(runner.RESULT)
            send_dding_msg(conf['MESSAGE']['TOKEN'], TMPL_MSG)

        if conf['MESSAGE']['EMAIL']:
            EmailClass().send()


if __name__=="__main__":
    run_min()

