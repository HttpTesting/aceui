import os
import unittest
import ddt
from pages import *
from aceui.lib.core import (
    select_Browser_WebDriver,
    reply_case_fail,
    get_data,
    join_url
)
from aceui.lib import (
    gl,
    HTMLTESTRunnerCN
)

'''
1.以上导入不需要动，pages导入的所有包名，引用：包名称.类名称
2.只需要改动以下代码
'''

@ddt.ddt
class TestActivityCreate64(unittest.TestCase):
    """营销－开卡关怀"""
    @classmethod
    def setUpClass(cls):
        cls.driver = select_Browser_WebDriver()
        cls.url = join_url('/activity/create/64')

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        # pass


    @ddt.data(*get_data('activityCreate64', 'CASE1'))
    @reply_case_fail(num=3)
    def testCase1(self, data):
        """开卡关怀"""
        print('========★{}★========'.format(data['case_desc'])) #case描述
        self.tc = activityCreate64.ActivityCreate64(
            self.url,
            self.driver,
            data['page_title']
        )
        self.tc.open
        #活动名称
        self.tc.input_activity_name(data['activity_name'])
        #赠券设置-增加券
        self.tc.click_add_coupon()
        #券类型;0代金券；1礼品券
        self.tc.click_coupon_type(data['coupon_type'])
        #使用
        self.tc.click_coupon_used(data['coupon_index'])
        #赠送积分
        self.tc.input_credit(data['credit_num'])
        #赠送储值
        self.tc.input_charge(data['charge_num'])
        #发券提醒;0不提醒；1短信提醒
        self.tc.click_send_remind(data['remind_index'])
        #券到期提醒;0不提醒；1短信提醒
        self.tc.click_expire(data['expire_index'])
        #活动卡类别
        self.tc.click_card_type()
        #活动开始时间－结束时间
        self.tc.input_start_time(data['start_time'])
        self.tc.input_end_time(data['end_time'])
        #保存-确认
        self.tc.click_save_button()
        self.tc.click_sconfirm_btn()
        #输入活动名称
        self.tc.input_search_name(data['activity_name'])
        #查询
        self.tc.click_search_button()
        #断言
        self.tc.assert_add_success(data['start_time'])
        #删除
        self.tc.click_delete_button()
        #断言列表为空
        self.assertTrue(self.tc.assert_delete_result())

