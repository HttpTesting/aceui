



PO模式 脚手架结构说明：

scaffold
|
├─data  存储数据参数化文件，不是必须
|
├─pages 存储页面元素定位
| |
| └─demoPage.py  元素定位，给件封装
|
└─testCase 存储测试用例执行py
| |
| └─── testDemo.py  测试case编写
|
└─debug.py  执行入口，执行该py，调用执行testCase下test开头的py文件
|
└─chromedriver.exe  浏览器驱动放在此目录