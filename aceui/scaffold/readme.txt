



PO模式 脚手架结构说明：

├─data  存储数据参数化文件，不是必须
├
├─pages 存储页面元素定位
| ├
| └─ demoPage.py  demo页元素定位对象
|
└─testCase 存储测试用例执行py
| ├
| └─ testDemo.py  demo测试case
|
└─debug.py 执行case用例入口，可以用于ide调试执行，会执行testCase目录下所有test开头的py文件