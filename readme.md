﻿<pre style="background-color:#2b2b2b;color:#218e23;font-family:'Courier New';font-size:12.0pt;">TestPySeUI使用说明
<br>

<br>一、TestPySeUI介绍
<br>    1、特点
<br>       (1)支持多种定位方法（id\name\class\link_text\xpath\css）。
<br>       (2)基于unittest单元测试框架，所以测试文件与测试方法遵循unittest开发。
<br>       (3)支持识别验证码。
<br>       (4)自动生成并发送HTML测试报告。
<br>
<br>    2、环境说明
<br>       Python3.5+ :https://www.python.org/
<br>       Selenium3.0.0+ :https://pypi.python.org/pypi/selenium
<br>
<br>    3、支持的浏览器及驱动
<br>       (1)浏览器
<br>          Firefox:
<br>          driver = PyseUI("firefox")  
<br>          或：
<br>          driver = PyseUI("ff")
<br>
<br>          Chrome:
<br>          driver = PyseUI("chrome")  
<br>
<br>          IE:
<br>          driver = PyseUI("internet explorer")
<br>          或：
<br>          driver = PyseUI("ie")
<br>
<br>          Opera:
<br>          driver = PyseUI("opera")
<br>
<br>          PhantomJS:
<br>          driver = PyseUI("phantomjs")
<br>
<br>          Edge:
<br>          driver = PyseUI("edge")
<br>
<br>       (2)浏览器驱动:
<br>          geckodriver(Firefox):https://github.com/mozilla/geckodriver/releases
<br>          Chromedriver(Chrome):https://sites.google.com/a/chromium.org/chromedriver/home
<br>          IEDriverServer(IE):http://selenium-release.storage.googleapis.com/index.html
<br>          operadriver(Opera):https://github.com/operasoftware/operachromiumdriver/releases
<br>          phantomjs(PhantomJS):http://phantomjs.org
<br>          MicrosoftWebDriver(Edge):https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver
<br>
<br>   4、元素定位
<br>      支持多种定位方式，id、name、class、link text、xpath和css。
<br>      ==========================================================
<br>      id定位:
<br>      driver.type("id=>kw", "TestPySeUI")
<br>      ==========================================================
<br>      class定位:
<br>      driver.type("class=>s_ipt", "TestPySeUI")
<br>      ==========================================================
<br>      name定位:
<br>      driver.type("name=>wd", "TestPySeUI")
<br>      ==========================================================
<br>      link text定位： 
<br>      driver.click_text(u"link_text=>新闻")
<br>      ==========================================================
<br>      xpath定位：
<br>      driver.type("xpath=>//*[@class='s_ipt']","TestPySeUI")
<br>      driver.type("xpath=>//*[@id='kw']","TestPySeUI")
<br>      ==========================================================
<br>      css定位：
<br>      driver.type("css=>.s_ipt","TestPySeUI")
<br>      driver.type("css=>#su","TestPySeUI")
<br>      ==========================================================
<br>
<br>      css选择器参考手册： http://www.w3school.com.cn/cssref/css_selectors.asp 
<br>
<br>二、TestPySeUI功能：
<br>    1、本框架整合了部分虫师的pyse和pyAutoForm的功能。对webdriver部分功能进行了二次封装，使用更加方便: public/common/pyseui.py
<br>    (ps：参考：https://github.com/defnngj/pyse、http://www.51testing.com/html/44/448544-3693918.html)
<br>    2、实现了对excel表进行数据读取: public/common/excel.py
<br>    3、实现了打印日志的功能，可打印在控制台和文件中。日志保存在report/log/目录下: public/common/log.py
<br>    4、实现了读取配置文件功能(.ini文件): public/common/readconfig.py
<br>    5、实现了随机生成个人姓名、身份证号和手机号的功能：public/common/person.py
<br>    6、实现了识别验证码功能（如果验证码是数字和字母组成的复杂验证码，识别率较低）：public/common/vcode.py
<br>    7、实现了发邮件的功能:public/common/sendmail.py
<br>    8、实现了生成HTM测试报告，报告保存在report/testreport/目录下：public/common/HTMLTestRunner.py
<br>    
<br>三、整个项目的目录结构:
<br>    ├─config 配置文件的目录
<br>    │  │  config.ini      # 存放配置文件
<br>    │  │  globalparam.py  # 重要的全局参数，如log、report、screenshot的路径配置等
<br>    │  │  __init__.py
<br>    │  │
<br>    │
<br>    ├─data   测试数据
<br>    │  ├─formaldata # 正式环境测试数据
<br>    │  └─testdata   # 测试环境的数据
<br>    │          districtcode.txt # 区域代码
<br>    │          case.xls         # 用例数据
<br>    │
<br>    ├─public  公共的文件库
<br>    │  │  __init__.py
<br>    │  │
<br>    │  ├─common  封装的公共方法
<br>    │  │  │  excel.py
<br>    │  │  │  HTMLTestRunner.py
<br>    │  │  │  log.py
<br>    │  │  │  person.py
<br>    │  │  │  pyseui.py
<br>    │  │  │  readconfig.py
<br>    │  │  │  sendmail.py
<br>    │  │  │  vcode.py
<br>    │  │  │  __init__.py
<br>    │  │  │
<br>    │  │
<br>    │  ├─pages 存放实际项目公共测试方法的目录
<br>    │  │  │  __init__.py
<br>    │
<br>    ├─report 测试报告
<br>    │  ├─screenshot # 截图目录
<br>    │  ├─log        # 日志目录
<br>    │  │      2017-08-31.log
<br>    │  │
<br>    │  └─testreport # html测试报告目录
<br>    │         百度搜索测试报告2017-08-31_15_27_09.html
<br>    │
<br>    └─testcase 存放测试用例目录
<br>        │  test_baidu.py
<br>    
<br>    
<br>四、使用说明:
<br>    1、安装依赖的库:
<br>       （1）pip install xlrd,selenium,configparser
<br>       （2）安装Pillow
<br>               下载地址：https://pypi.python.org/pypi/Pillow/3.3.0
<br>               安装包Pillow-3.3.0-cp27-cp27m-win_amd64.whl
<br>              pip install Pillow-3.3.0-cp27-cp27m-win_amd64.whl
<br>        注意：需要将C:\Python27\Scripts加入系统环境变量中。
<br>       （3）安装Tesseract
<br>            地址：http://jaist.dl.sourceforge.net/project/tesseract-ocr-alt/tesseract-ocr-setup-3.02.02.exe
<br>    2、在config.ini中配置项目路径：project_path
<br>    3、在glableparam.py中配置默认浏览器、邮件服务器、邮件发送人和接收人等
<br>    4、使用的用例数据放在data/testdata/case.xls中
<br>    5、在testcase目录下面，编写测试用例，可以分模块编写，建相应的目录
<br>    6、执行run.py,就可以执行所有的测试用例
<br>    6、在report/log里面查看日志
<br>    7、在report/testreport里面查看html测试报告
<br>    
<br>五、关于pyseui的使用:
<br>        该py文件是根据虫师pyse整合，根据自己的需求加了一些函数。如识别验证码、随机生成姓名、读取excel等
<br>        参考虫师的github地址:https://github.com/defnngj/pyse
<br>          
<br>    1、启动谷歌浏览器
<br>       dr = pyseui.PySeUI('chrome')
<br>       启动远程浏览器
<br>       dr = pyseui.PySeUI(RChrome','127.0.0.1:8080')
<br>    2、地址栏输入网址：
<br>       dr.open('http://www.baidu.com')
<br>    3、刷新浏览器：
<br>       driver.F5()
<br>    4、关闭浏览器：
<br>       driver.close()
<br>    5、退出浏览器：
<br>       driver.quit()
<br>    6、获取浏览器窗口标题：
<br>       driver.get_window_title()
<br>    7、获取浏览器窗口url：
<br>       driver.get_window_url()
<br>    8、窗口最大化：
<br>       driver.set_window_max()
<br>    9、设置浏览器的窗口大小
<br>       dr.set_window_size(800,500)
<br>    10、点击元素并打开新窗口
<br>       driver.open_new_window("id-&gt;kw")
<br>    11、切换到最新打开的窗口
<br>       dirver.switch_to_new_window()
<br>    12、设置当前窗口作为默认窗口
<br>       driver.set_current_window_as_default()
<br>    13、切换到默认窗口
<br>       driver.switch_to_default_window()
<br>    14、关闭当前窗口以外的窗口
<br>       driver.close_other_windows()
<br>    15、等待某个元素显示
<br>       driver.wait_element("id-&gt;kw",10)
<br>    16、定位元素
<br>       driver.get_element('id-&gt;kw')
<br>    17、输入内容
<br>       driver.type("id-&gt;kw","selenium")
<br>    18、输入内容并回车
<br>       driver.type_css_keys('id-&gt;kw','selenium')
<br>    19、清除内容
<br>       driver.clear("css-&gt;kw")
<br>    20、清除输入框并输入内容
<br>       driver.clear_type("id-&gt;kw","selenium")
<br>    21、单击
<br>       driver.click("id-&gt;kw")
<br>    22、双击
<br>       driver.double_click("id-&gt;kw")
<br>    23、右击
<br>    …………………………
<br>    
<br>六、关于excel的使用:
<br>    1、初始化excel
<br>       xls = excel.Excel(xls_file)
<br>    2、根据sheet名称读取指定行、列、长度的数据
<br>       xls.getDatasByRow(u"sheet名称",1,3,3)
<br>    3、根据sheet名称读取指定列、列、长度的数据
<br>    …………………………
<br>    
<br>七、关于person的使用:    
<br>    1、初始化person
<br>       p = person.Person()
<br>    …………………………
<br>    
<br>八、关于vcode的使用:  
<br>    1、初始化vcode
<br>    …………………………
<br>    
<br>九、关于log的使用: 
<br>    1、初始化log
<br>       log = log.Log()
<br>    2、打印调试信息
<br>       log.debug()
<br>    3、打印一般信息
<br>    …………………………
<br>
<br>
<br>
<br>    Email:363060259@qq.com