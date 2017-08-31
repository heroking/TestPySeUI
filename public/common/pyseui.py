# coding=utf-8

import time
import os
import urllib2
import datetime
import filecmp
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import ui
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.alert import Alert
from selenium.common.exceptions import TimeoutException
from public.common.log import Log
from config import globalparam

success = "SUCCESS   "
fail = "FAIL   "
logger = Log()

class PySeUI(object):
    """
        pyselenium framework for the main class, the original
    selenium provided by the method of the two packaging,
    making it easier to use.
    """

    def __init__(self, browser='ff', remoteAddress=None):
        """
        remote consle：
        dr = PySelenium('RChrome','127.0.0.1:8080')
        """
        t1 = time.time()
        dc = {'platform': 'ANY', 'browserName': 'chrome', 'version': '', 'javascriptEnabled': True}
        options = webdriver.ChromeOptions()
        options.add_experimental_option("excludeSwitches", ["ignore-certificate-errors"])
        dr = None
        if remoteAddress is None:
            if browser == "firefox" or browser == "ff":
                dr = webdriver.Firefox()
            elif browser == "chrome" or browser == "Chrome":
                dr = webdriver.Chrome(options)
            elif browser == "internet explorer" or browser == "ie":
                dr = webdriver.Ie()
            elif browser == "opera":
                dr = webdriver.Opera()
            elif browser == "phantomjs":
                dr = webdriver.PhantomJS()
            elif browser == "edge":
                dr = webdriver.Edge()
        else:
            if browser == "RChrome":
                dr = webdriver.Remote(command_executor='http://' + remoteAddress + '/wd/hub',
                                      desired_capabilities=dc)
            elif browser == "RIE":
                dc['browserName'] = 'internet explorer'
                dr = webdriver.Remote(command_executor='http://' + remoteAddress + '/wd/hub',
                                      desired_capabilities=dc)
            elif browser == "RFirefox":
                dc['browserName'] = 'firefox'
                dc['marionette'] = False
                dr = webdriver.Remote(command_executor='http://' + remoteAddress + '/wd/hub',
                                      desired_capabilities=dc)
        try:
            self.driver = dr
            self.my_print("{0} Start a new browser: {1}, Spend {2} seconds".format(success,browser,time.time()-t1))
        except Exception:
            raise NameError("Not found {0} browser,You can enter 'ie','ff',"
                            "'chrome','RChrome','RIe' or 'RFirefox'.".format( browser))
    @property
    def origin_driver(self):
        """
        Return the original driver,Can use webdriver API.

        Usage:
        driver.origin_driver
        """
        return self.driver
    
    def open(self, url):
        """
        open url.

        Usage:
        driver.open("https://www.baidu.com")
        """
        t1 = time.time()
        try:
            self.driver.get(url)
            self.my_print("{0} Navigated to {1}, Spend {2} seconds".format(success,url,time.time()-t1))
        except Exception:
            self.my_print("{0} Unable to load {1}, Spend {2} seconds".format(fail, url, time.time() - t1))
            raise

    def F5(self):
        """
        Refresh the current page.

        Usage:
        driver.F5()
        """
        t1 = time
        self.driver.refresh()
        self.my_print("{0} Refresh the current page, Spend {1} seconds".format(success, time.time() - t1))
               
    def close(self):
        """
        Simulates the user clicking the "close" button in the titlebar of a popup
        window or tab.

        Usage:
        driver.close()
        """
        t1 = time.time()
        self.driver.close()
        self.my_print("{0} Closed current window, Spend {1} seconds".format(success, time.time() - t1))

    def quit(self):
        """
        Quit the driver and close all the windows.

        Usage:
        driver.quit()
        """
        t1 = time.time()
        self.driver.quit()
        self.my_print("{0} Closed all window and quit the driver, Spend {1} seconds".format(success, time.time() - t1))

    def get_window_title(self):
        """
        Get window title.

        Usage:
        driver.get_window_title()
        """

        t1 = time.time()
        title = self.driver.title
        self.my_print("{0} Get current window title, Spend {1} seconds".format(success, time.time() - t1))
        return title

    def get_window_url(self):
        """
        Get the URL address of the current page.

        Usage:
        driver.get_window_url()
        """
        t1 = time.time()
        url = self.driver.current_url
        self.my_print("{0} Get current window url, Spend {1} seconds".format(success, time.time() - t1))
        return url

    def set_window_max(self):
        """
        Set browser window maximized.

        Usage:
        driver.set_window_max()
        """
        t1 = time.time()
        self.driver.maximize_window()
        self.my_print("{0} Set browser window maximized, Spend {1} seconds".format(success, time.time() - t1))

    def set_window_size(self, wide, high):
        """
        Set browser window wide and high.

        Usage:
        driver.set_window(wide,high)
        """
        t1 = time.time()
        self.driver.set_window_size(wide, high)
        self.my_print("{0} Set browser window wide: {1},high: {2}, Spend {3} seconds".format(success,
            wide,high,time.time() - t1))

    def open_new_window(self, css):
        """
        Open the new window and switch the handle to the newly opened window.

        Usage:
        driver.open_new_window("id->kw")
        """
        t1 = time.time()
        try:
            original_windows = self.driver.current_window_handle
            el = self.get_element(css)
            el.click()
            all_handles = self.driver.window_handles
            for handle in all_handles:
                if handle != original_windows:
                    self.driver.switch_to.window(handle)
            self.my_print("{0} Click element: <{1}> open a new window and swich into, Spend {2} seconds".format(success,
                css,time.time() - t1))
        except Exception:
            self.my_print("{0} Click element: <{1}> open a new window and swich into, Spend {2} seconds".format(fail,
                css,time.time() - t1))
            raise

    def switch_to_new_window(self):
        """
        Into the new window.

        Usage:
        dirver.switch_to_new_window()
        """
        t1 = time.time()
        try:
            all_handle = self.driver.window_handles
            flag = 0
            while len(all_handle) < 2:
                time.sleep(1)
                all_handle = self.driver.window_handles
                flag += 1
                if flag == 5:
                    break
            self.driver.switch_to.window(all_handle[-1])
            self.my_print("{0} Switch to the new window,new window's url: {1}, Spend {2} seconds".format(success,
                self.driver.current_url,time.time() - t1))
        except Exception:
            self.my_print("{0} Unable switch to the new window, Spend {1} seconds".format(fail, time.time() - t1))
            raise

    def set_current_window_as_default(self):
        '''
                            设置当前窗口作为默认窗口
                                                    
                            使用:
        driver.set_current_window_as_default()
        '''
        result = {}
        try:
            self.setDefaultWindow(self.driver.current_window_handle)
            self.setCurrentWindow(self.driver.current_window_handle)
            result = True
        except Exception as e:
            result = False
        return result

    def switch_to_default_window(self):
        '''
                            切换到默认窗口
                                                    
                            使用:
        driver.switch_to_default_window()
        '''
        result = {}
        try:
            self.driver.switch_to.window(self.getDefaultWindow())
            self.setCurrentWindow(self.driver.current_window_handle)
            result = True
        except Exception as e:
            result = False
        return result
    
    def close_other_windows(self):
        '''
                            关闭当前窗口以外的窗口
                                                    
                            使用:
        driver.close_other_windows()
        '''
        result = {}
        try:
            allWindows = self.driver.window_handles
            for i in range(0, allWindows.__len__()):
                tempWindow = allWindows.__getitem__(i)
                if (self.currentWindow <> tempWindow):
                    self.driver.switch_to.window(tempWindow)
                    self.driver.close()
                self.driver.switch_to.window(self.currentWindow)
                self.setDefaultWindow(self.driver.current_window_handle)
                self.setCurrentWindow(self.driver.current_window_handle)
                result = True
        except Exception as e:
            result = False
        return result
    
    def wait_element(self, css, secs=5):
        """
        Waiting for an element to display.

        Usage:
        driver.wait_element("id->kw",10)
        """
        if "->" not in css:
            raise NameError("Positioning syntax errors, lack of '->'.")

        by = css.split("->")[0].strip()
        value = css.split("->")[1].strip()
        messages = 'Element: {0} not found in {1} seconds.'.format(css, secs)

        if by == "id":
            WebDriverWait(self.driver, secs, 1).until(EC.presence_of_element_located((By.ID, value)), messages)
        elif by == "name":
            WebDriverWait(self.driver, secs, 1).until(EC.presence_of_element_located((By.NAME, value)), messages)
        elif by == "class":
            WebDriverWait(self.driver, secs, 1).until(EC.presence_of_element_located((By.CLASS_NAME, value)), messages)
        elif by == "link_text":
            WebDriverWait(self.driver, secs, 1).until(EC.presence_of_element_located((By.LINK_TEXT, value)), messages)
        elif by == "xpath":
            WebDriverWait(self.driver, secs, 1).until(EC.presence_of_element_located((By.XPATH, value)), messages)
        elif by == "css":
            WebDriverWait(self.driver, secs, 1).until(EC.presence_of_element_located((By.CSS_SELECTOR, value)),messages)
        else:
            raise NameError("Please enter the correct targeting elements,'id','name','class','link_text','xpaht','css'.")

    def get_element(self, css):
        """
        Judge element positioning way, and returns the element.

        Usage:
        driver.get_element('id->kw')
        """
        if "->" not in css:
            raise NameError("Positioning syntax errors, lack of '->'.")

        by = css.split("->")[0].strip()
        value = css.split("->")[1].strip()

        if by == "id":
            element = self.driver.find_element_by_id(value)
        elif by == "name":
            element = self.driver.find_element_by_name(value)
        elif by == "class":
            element = self.driver.find_element_by_class_name(value)
        elif by == "link_text":
            element = self.driver.find_element_by_link_text(value)
        elif by == "xpath":
            element = self.driver.find_element_by_xpath(value)
        elif by == "css":
            element = self.driver.find_element_by_css_selector(value)
        else:
            raise NameError("Please enter the correct targeting elements,'id','name','class','link_text','xpaht','css'.")
        return element


    def type(self, css, text):
        """
        Operation input box.

        Usage:
        driver.type("id->kw","selenium")
        """
        t1 = time.time()
        try:
            self.element_wait(css)
            el = self.get_element(css)
            el.send_keys(text)
            self.my_print("{0} Typed element: <{1}> content: {2}, Spend {3} seconds".format(success,
                css,text,time.time() - t1))
        except Exception:
            self.my_print("{0} Unable to type element: <{1}> content: {2}, Spend {3} seconds".format(fail,
                css, text, time.time() - t1))
            raise

    def type_and_enter(self, css, text, secs=0.5):
        """
        Operation input box. 1、input message,sleep 0.5s;2、input ENTER.

        Usage:
        driver.type_css_keys('id->kw','beck')
        """
        t1 = time.time()
        try:
            self.element_wait(css)
            ele = self.get_element(css)
            ele.send_keys(text)
            time.sleep(secs)
            ele.send_keys(Keys.ENTER)
            self.my_print("{0} Element <{1}> type content: {2},and sleep {3} seconds,input ENTER key, Spend {4} seconds".format(
                success,css,text,secs,time.time() - t1))
        except Exception:
            self.my_print("{0} Unable element <{1}> type content: {2},and sleep {3} seconds,input ENTER key, Spend {4} seconds".
                format(fail, css, text, secs, time.time() - t1))
            raise
                
    def clear(self, css):
        '''
        Clear the contents of the input box.

        Usage:
        driver.clear("css->kw")
        '''
        t1 = time.time()
        try:
            self.element_wait(css)
            el = self.get_element(css)
            el.clear()
            self.my_print("{0} Cleared element: <{1}> content: {2}, Spend {3} seconds".format(success,
                css,el.text,time.time() - t1))
        except Exception:
            self.my_print("{0} Unable to Clear element: <{1}> content: {2}, Spend {3} seconds".format(fail,
                css,el.text, time.time() - t1))
            raise

    def clear_type(self, css, text):
        """
        Clear and input element.

        Usage:
        driver.clear_type("id->kw","selenium")
        """
        t1 = time.time()
        try:
            self.element_wait(css)
            el = self.get_element(css)
            el.clear()
            el.send_keys(text)
            self.my_print("{0} Clear and type element: <{1}> content: {2}, Spend {3} seconds".format(success,
                css, text,time.time() - t1))
        except Exception:
            self.my_print("{0} Unable to clear and type element: <{1}> content: {2}, Spend {3} seconds".format(fail,
                css, text,time.time() - t1))
            raise

    def click(self, css):
        """
        It can click any text / image can be clicked
        Connection, check box, radio buttons, and even drop-down box etc..

        Usage:
        driver.click("id->kw")
        """
        t1 = time.time()
        try:
            self.element_wait(css)
            el = self.get_element(css)
            el.click()
            self.my_print("{0} Clicked element: <{1}>, Spend {2} seconds".format(success,css,time.time() - t1))
        except Exception:
            self.my_print("{0} Unable to click element: <{1}>, Spend {2} seconds".format(fail, css, time.time() - t1))
            raise

    def double_click(self, css):
        """
        Double click element.

        Usage:
        driver.double_click("id->kw")
        """
        t1 = time.time()
        try:
            self.element_wait(css)
            el = self.get_element(css)
            ActionChains(self.driver).double_click(el).perform()
            self.my_print("{0} Double click element: <{1}>, Spend {2} seconds".format(success, css, time.time() - t1))
        except Exception:
            self.my_print("{0} Unable to double click element: <{1}>, Spend {2} seconds".format(fail, css, time.time() - t1))
            raise

    def right_click(self, css):
        """
        Right click element.

        Usage:
        driver.right_click("id->kw")
        """
        t1 = time.time()
        try:
            self.element_wait(css)
            el = self.get_element(css)
            ActionChains(self.driver).context_click(el).perform()
            self.my_print("{0} Right click element: <{1}>, Spend {2} seconds".format(success, css, time.time() - t1))
        except Exception:
            self.my_print("{0} Unable to right click element: <{1}>, Spend {2} seconds".format(fail, css, time.time() - t1))
            raise

    def click_and_hold(self,css):
        """
                            点击并按住元素不放.

                            使用:
        driver.click_and_hold("id->kw")
        """
        t1 = time.time()
        try:
            self.element_wait(css)
            el = self.get_element(css)
            ActionChains(driver).click_and_hold(el).perform()
            self.my_print("{0} click and hold element: <{1}>, Spend {2} seconds".format(success, css, time.time() - t1))
        except Exception:
            self.my_print("{0} Unable to click and hold element: <{1}>, Spend {2} seconds".format(fail, css, time.time() - t1))
            raise
        
    def move_to_element(self, css):
        """
        Mouse over the element.

        Usage:
        driver.move_to_element("id->kw")
        """
        t1 = time.time()
        try:
            self.element_wait(css)
            el = self.get_element(css)
            ActionChains(self.driver).move_to_element(el).perform()
            self.my_print("{0} Move to element: <{1}>, Spend {2} seconds".format(success, css, time.time() - t1))
        except Exception:
            self.my_print("{0} unable move to element: <{1}>, Spend {2} seconds".format(fail, css, time.time() - t1))
            raise

    def scroll_to_element(self, css):
        '''
                            滚轮滚动到对应元素.

                            使用:
        driver.scroll_to_element("id->kw")
        '''
        t1 = time.time()
        try:
            self.element_wait(css)
            el = self.get_element(css)
            scrollto = "window.scrollTo(" + str(el.location.get("x")) + "," + str(
                el.location.get("y")) + ")"
            self.driver.execute_script(scrollto)
        except Exception as e:
            print e.message

    def drag_and_drop(self, el_css, ta_css):
        """
                           拖拽元素1到元素2

        Usage:
        driver.drag_and_drop("id->kw","id->su")
        """
        t1 = time.time()
        try:
            self.element_wait(el_css)
            element = self.get_element(el_css)
            self.element_wait(ta_css)
            target = self.get_element(ta_css)
            ActionChains(driver).drag_and_drop(element, target).perform()
            self.my_print("{0} Drag and drop element: <{1}> to element: <{2}>, Spend {3} seconds".format(success,
                el_css,ta_css, time.time() - t1))
        except Exception:
            self.my_print("{0} Unable to drag and drop element: <{1}> to element: <{2}>, Spend {3} seconds".format(fail,
                el_css, ta_css, time.time() - t1))
            raise

    def click_text(self, text):
        """
        Click the element by the link text

        Usage:
        driver.click_text("新闻")
        """
        t1 = time.time()
        try:
            self.driver.find_element_by_partial_link_text(text).click()
            self.my_print("{0} Click by text content: {1}, Spend {2} seconds".format(success, text,time.time() - t1))
        except Exception:
            self.my_print("{0} Unable to Click by text content: {1}, Spend {2} seconds".format(fail, text, time.time() - t1))
            raise

    def text_contains(self, css, text):
        """
                            判断是否包含指定text内容

                            使用:
        driver.text_contains("id->kw",text)
        """
        t1 = time.time()
        try:
            self.element_wait(css)
            el = self.get_element(css)
            t_text = el.text
            if (t_text.__contains__(text)):
                self.my_print("{0} Element: <{1}> is contains text, Spend {2} seconds".format(success,css, time.time() - t1))
                return True
            else:
                self.my_print("{0} Element: <{1}> is not contains text, Spend {2} seconds".format(fail, css, time.time() - t1))
                return False 
        except TimeoutException:
            self.my_print("{0} Element: <{1}> is not contains text, Spend {2} seconds".format(fail, css, time.time() - t1))
            return False   
        
    def submit(self, css):
        """
        Submit the specified form.

        Usage:
        driver.submit("id->kw")
        """
        t1 = time.time()
        try:
            self.element_wait(css)
            el = self.get_element(css)
            el.submit()
            self.my_print("{0} Submit form args element: <{1}>, Spend {2} seconds".format(success,css, time.time() - t1))
        except Exception:
            self.my_print("{0} Unable to submit form args element: <{1}>, Spend {2} seconds".format(fail, css, time.time() - t1))
            raise

    def js(self, script):
        """
        Execute JavaScript scripts.

        Usage:
        driver.js("window.scrollTo(200,1000);")
        """
        t1 = time.time()
        try:
            self.driver.execute_script(script)
            self.my_print("{0} Execute javascript scripts: {1}, Spend {2} seconds".format(success,script, time.time() - t1))
        except Exception:
            self.my_print("{0} Unable to execute javascript scripts: {1}, Spend {2} seconds".format(fail,
                script, time.time() - t1))
            raise

    def js_click(self, css):
        """
        Input a css selecter,use javascript click element.

        Usage:
        driver.js_click('#buttonid')
        """
        t1 = time.time()
        js_str = "$('{0}').click()".format(css)
        try:
            self.driver.execute_script(js_str)
            self.my_print("{0} Use javascript click element: {1}, Spend {2} seconds".format(success,js_str,time.time()-t1))
        except Exception:
            self.my_print("{0} Unable to use javascript click element: {1}, Spend {2} seconds".format(fail,
                js_str, time.time() - t1))
            raise
        
    def get_attribute(self, css, attribute):
        """
        Gets the value of an element attribute.

        Usage:
        driver.get_attribute("id->su","href")
        """
        t1 = time.time()
        try:
            el = self.get_element(css)
            attr = el.get_attribute(attribute)
            self.my_print("{0} Get attribute element: <{1}>,attribute: {2}, Spend {3} seconds".format(success,
                css,attribute,time.time()-t1))
            return attr
        except Exception:
            self.my_print("{0} Unable to get attribute element: <{1}>,attribute: {2}, Spend {3} seconds".format(fail,
                css, attribute,time.time() - t1))
            raise

    def get_text(self, css):
        """
        Get element text information.

        Usage:
        driver.get_text("id->kw")
        """
        t1 = time.time()
        try:
            self.element_wait(css)
            text = self.get_element(css).text
            self.my_print("{0} Get element text element: <{1}>, Spend {2} seconds".format(success,css,time.time()-t1))
            return text
        except Exception:
            self.my_print("{0} Unable to get element text element: <{1}>, Spend {2} seconds".format(fail, css, time.time() - t1))
            raise

    def get_display(self, css):
        '''
        Gets the element to display,The return result is true or false.

        Usage:
        driver.get_display("id->kw")
        '''
        t1 = time.time()
        try:
            self.element_wait(css)
            el = self.get_element(css)
            self.my_print("{0} Get element display element: <{1}>, Spend {2} seconds".format(success,css,time.time()-t1))
            return el.is_displayed()
        except Exception:
            self.my_print("{0} Unable to get element display element: <{1}>, Spend {2} seconds".format(fail, css, time.time() - t1))
            raise

    def wait(self, secs):
        """
        Implicitly wait.All elements on the page.

        Usage:
        driver.wait(10)
        """
        t1 = time.time()
        self.driver.implicitly_wait(secs)
        self.my_print("{0} Set wait all element display in {1} seconds, Spend {2} seconds".format(success,
            secs,time.time() - t1))

    def accept_alert(self):
        """
        Accept warning box.

        Usage:
        driver.accept_alert()
        """
        t1 = time.time()
        self.driver.switch_to.alert.accept()
        self.my_print("{0} Accept warning box, Spend {1} seconds".format(success, time.time() - t1))

    def dismiss_alert(self):
        """
        Dismisses the alert available.

        Usage:
        driver.dismiss_alert()
        """
        t1 = time.time()
        self.driver.switch_to.alert.dismiss()
        self.my_print("{0} Dismisses the alert available, Spend {1} seconds".format(success, time.time() - t1))

    @staticmethod
    def select_checkbox(self,css,flag=1):
        """
                            复选框选中及不选中操作(0不选,>0选中)

                            使用:
        driver.select_checkbox("id->kw",flag)
        """
        t1 = time.time()
        try:
            self.element_wait(css)
            el = self.get_element(css)
            
            if not el.is_selected():
                if(flag>0):
                    el.click()
            else:
                if(flag==0):
                    el.click()
            self.my_print("{0} select the checkbox element: <{1}>, Spend {2} seconds".format(success, css, time.time() - t1))
        except Exception:
            self.my_print("{0} Unable to select the checkbox element: <{1}>, Spend {2} seconds".format(fail, css, time.time() - t1))
            raise
        

    @staticmethod
    def select_by_index(self,css,index):
        """
                            根据index选择下拉菜单数据

                            使用:
        driver.select_by_index("id->kw",index)
        """
        t1 = time.time()
        try:
            self.element_wait(css)
            el = self.get_element(css)
            ui.Select(el).select_by_index(index)
            self.my_print("{0} select drop-down list element: <{1}>, Spend {2} seconds".format(success, css, time.time() - t1))
        except Exception:
            self.my_print("{0} Unable to select drop-down list element: <{1}>, Spend {2} seconds".format(fail, css, time.time() - t1))
            raise
                
    @staticmethod
    def select_by_text(self,css,text):
        """
                            根据text选择下拉菜单数据

                            使用:
        driver.select_by_text("id->kw",text)
        """
        t1 = time.time()
        try:
            self.element_wait(css)
            el = self.get_element(css)
            ui.Select(el).select_by_visible_text(text)
            self.my_print("{0} select drop-down list element: <{1}>, Spend {2} seconds".format(success, css, time.time() - t1))
        except Exception:
            self.my_print("{0} Unable to select drop-down list element: <{1}>, Spend {2} seconds".format(fail, css, time.time() - t1))
            raise

    @staticmethod
    def select_by_value(self,css,value):
        """
                            根据value选择下拉菜单数据

                            使用:
        driver.select_by_value("id->kw",value)
        """
        t1 = time.time()
        try:
            self.element_wait(css)
            el = self.get_element(css)
            ui.Select(el).select_by_value(value)
            self.my_print("{0} select drop-down list element: <{1}>, Spend {2} seconds".format(success, css, time.time() - t1))
        except Exception:
            self.my_print("{0} Unable to select drop-down list element: <{1}>, Spend {2} seconds".format(fail, css, time.time() - t1))
            raise
        
    def is_element_exist(self, css):
        """
        judge element is exist,The return result is true or false.

        Usage:
        driver.element_exist("id->kw")
        """
        t1 = time.time()
        try:
            self.element_wait(css)
            self.my_print("{0} Element: <{1}> is exist, Spend {2} seconds".format(success,css, time.time() - t1))
            return True
        except TimeoutException:
            self.my_print("{0} Element: <{1}> is not exist, Spend {2} seconds".format(fail, css, time.time() - t1))
            return False

    def is_text_equals(self,css,text):
        """
                            判断元素text内容是否等于text，等于返回True，不等于返回False

                            使用:
        driver.is_text_equals("id->kw",text)
        """
        try:
            self.element_wait(css)
            el = self.get_element(css)
            disText = el.text
            if ( text.strip()==disText):
                return True
            else:
                return False
        except Exception as e:
            return False

    def is_value_equals(self,css,value):
        """
                            判断元素value属性值是否等于value，等于返回True，不等于返回False

                            使用:
        driver.is_value_equals("id->kw",value)
        """
        try:
            self.element_wait(css)
            el = self.get_element(css)
            disValue = el.get_attribute("value")
            if (value==disValue):
                return True
            else:
                return False
        except Exception as e:
            return False

    def is_exist_secs(self,css,secs):
        """
                            判断元素在secs时间是否存在，存在返回True，不存在返回False

                            使用:
        driver.is_exist_secs("id->kw",secs)
        """
        try:
            t = 0
            disState = False
            while (t <= secs):
                if (self.is_element_exist(css)):
                    disState = True
                    break
                else:
                    time.sleep(0.25)
                    t = t + 0.25
            if (disState):
                return True
            else:
                return False
        except Exception as e:
            return False

    def is_displayed(self,css,value):
        """
                            判断元素是否显示，显示返回True，不显示返回False

                            使用:
        driver.is_displayed("id->kw","yes")
        """
        try:
            self.element_wait(css)
            el = self.get_element(css)
            disState=el.is_displayed()
            if (disState and value.lower()==self.YES):
                return True
            elif((not disState) and value.lower()==self.NO):
                return True
            else:
                return False
        except Exception as e:
            return False

    def is_selected(self,css,value):
        """
                            判断元素是否选中，选中返回True，不选中返回False

                            使用:
        driver.is_selected("id->kw","yes")
        """
        try:
            self.element_wait(css)
            el = self.get_element(css)
            disState=el.is_selected()
            if (disState and value.lower()==self.YES):
                return True
            elif((not disState) and value.lower()==self.NO):
                return True
            else:
                return False
        except Exception as e:
            return False

    def is_enabled(self,css,value):
        """
                            判断元素是否可操作，可操作返回True，不可操作返回False

                            使用:
        driver.is_enabled("id->kw","yes")
        """
        try:
            self.element_wait(css)
            el = self.get_element(css)
            disState=el.is_enabled()
            if (disState and value.lower()==self.YES):
                return True
            elif((not disState) and value.lower()==self.NO):
                return True
            else:
                return False
        except Exception as e:
            return False
    
    def take_screenshot(self, file_path):
        """
        Get the current window screenshot.

        Usage:
        driver.take_screenshot('c:/test.png')
        """
        t1 = time.time()
        try:
            self.driver.get_screenshot_as_file(file_path)
            self.my_print("{0} Get the current window screenshot,path: {1}, Spend {2} seconds".format(success,
                file_path, time.time() - t1))
        except Exception:
            self.my_print("{0} Unable to get the current window screenshot,path: {1}, Spend {2} seconds".format(fail,
                file_path,time.time() - t1))
            raise
        
    def switch_to_frame(self, css):
        """
        Switch to the specified frame.

        Usage:
        driver.switch_to_frame("id->kw")
        """
        t1 = time.time()
        try:
            self.element_wait(css)
            iframe_el = self.get_element(css)
            self.driver.switch_to.frame(iframe_el)
            self.my_print("{0} Switch to frame element: <{1}>, Spend {2} seconds".format(success,css, time.time() - t1))
        except Exception:
            self.my_print("{0} Unable switch to frame element: <{1}>, Spend {2} seconds".format(fail, css, time.time() - t1))
            raise

    def switch_to_frame_out(self):
        """
                          从frame中切回主文档(离开iframe，回到原来的地方)

                            使用:
        driver.switch_to_frame_out()
        """
        t1 = time.time()
        self.driver.switch_to.default_content()
        self.my_print("{0} Switch to frame out, Spend {1} seconds".format(success, time.time() - t1))


    def log(self,msg):
        """
                            打印日志功能

                            使用:
        driver.log("msg")
        """
        logger.info(msg)
        
    @staticmethod
    def get_cookie_string(self):
        """
                            获取cookie字符串

                            使用:
        driver.get_cookie_string()
        """
        Cookie=driver.get_cookies()
        tmp=""
        for c in Cookie:
            tmp=tmp+c["name"]+"="+c["value"]+"; "
        return tmp

    @staticmethod
    def modify_cookie(self, name, value=None, path=None, domain=None, secure=None, expiry=None):
        """
                            添加修改cookie

                            使用:
        driver.modify_cookie(name, value, path, domain, secure, expiry)
        """
        cookie = driver.get_cookie(name)
        _value = value
        _path = path
        _domain = domain
        _secure = secure
        _expiry = expiry
        if cookie:
            if not _value:
                _value = cookie["value"]
            if not _path:
                _path = cookie["path"]
            if not _domain:
                _domain = cookie["domain"]
            if not _secure:
                _secure = cookie["secure"]
            if not _expiry:
                _expiry = "Session"
            driver.delete_cookie(name)
        cookie_dic = {"name": name, "value": _value, "path":_path, "domain":_domain, "expiry":_expiry, "secure":_secure}
        driver.add_cookie(cookie_dic)
        
    @staticmethod
    def upload_file(self,css,filePath):
        """
                            上传文件

                            使用:
        driver.upload_file("id->kw",filePath)
        """
        t1 = time.time()
        try:
            self.element_wait(css)
            el = self.get_element(css)
            filePath=os.path.abspath(filePath)
            el.send_keys(filePath)
            self.my_print("{0} Upload file element: <{1}>, Spend {2} seconds".format(success, css, time.time() - t1))
        except Exception:
            self.my_print("{0} Unable to upload file element: <{1}>, Spend {2} seconds".format(fail, css, time.time() - t1))
            raise
        
    def same_as_localfile(self,css,localfile,proxy=""):
        """
                            下载网络文件与本地文件一致，仅限img标签与a标签;非WebDriver处理方法

                            使用:
        driver.same_as_localfile("id->kw",localfile,proxy="")
        """
        try:
            self.element_wait(css)
            el = self.get_element(css)
            tagName=el.tag_name
            if(tagName.lower()=="img"):
                urlPath=el.get_attribute("src")
            elif(tagName.lower()=="a"):
                urlPath=el.get_attribute("href")
            else:
                raise ValueError("the elemnet's tag is neither <img> nor <a>!")
            localFileDir=os.path.abspath(os.path.dirname(localfile))
            #检查是否存在下载临时文件夹及临时文件，没有的话，创建一个
            tempDir=os.path.join(localFileDir,"temp")
            if(not os.path.exists(tempDir)):
                os.makedirs(tempDir)
            tempFile=os.path.join(tempDir,"tmp"+datetime.datetime.now().strftime("%Y%m%d%H%M%S"))
 
            if(os.path.exists(tempFile)):
                os.remove(tempFile)
            #下载文件到临时文件夹
            cookieStr=self.get_cookie_string(self.driver)
            if(proxy=="" or proxy==None):
                opener = urllib2.build_opener()
            else:
                proxy_handler = urllib2.ProxyHandler({"http" : proxy})
                opener = urllib2.build_opener(proxy_handler)
            opener.addheaders.append(("Cookie", cookieStr))
            #print cookieStr
            f = opener.open(urlPath)
            with open(tempFile, "wb") as stream:
                stream.write(f.read())
            time.sleep(5)
            #比较
            rs=filecmp.cmp(tempFile, localfile, 1)
            if(rs):
                result = True
            else:
                result = False
            if(os.path.exists(tempDir)):
                import shutil
                shutil.rmtree(tempDir)
        except Exception as e:
            result = False
        return result
    
if __name__ == '__main__':
    driver = PySeUI("chrome")
