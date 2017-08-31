# -*- coding: utf-8 -*-
'''
Created on 2017-6-7

@author: whj
'''

import time
import re
from PIL import Image,ImageEnhance
import os
import subprocess
from config import globalparam

class VCode(object):
    def __init__(self, login_filePath, code_filePath):
        if (login_filePath and code_filePath):
            self.login_filePath = login_filePath
            self.code_filePath = code_filePath
        else:
            self.login_filePath = globalparam.img_path + "\\login\\login_file.jpg"
            self.code_filePath = globalparam.img_path + "\\login\\vcode_file.jpg"

    def setLoginFilePath(self, login_filePath):
        self.login_filePath = login_filePath
        
    def setCodeFilePath(self, code_filePath):
        self.code_filePath = code_filePath
        
    def getLoginFilePath(self):
        return self.login_filePath

    def getCodeFilePath(self):
        return self.code_filePath
    
    def __image_to_string(self,img, cleanup=True, plus=''):
        # cleanup为True则识别完成后删除生成的文本文件
        # plus参数为给tesseract的附加高级参数
        subprocess.check_output('tesseract ' + img + ' ' +
                                img + ' ' + plus, shell=True)  # 生成同名txt文件
        text = ''
        with open(img + '.txt', 'r') as f:
            text = f.read().strip()
        if cleanup:
            os.remove(img + '.txt')
        return text
    
    def getCode(self):  
        """
                            获取验证码，返回结果是4位的验证码
        """
        login_file = self.login_filePath
        code_file = self.code_filePath
        #-------------------对验证码进行区域截图，好吧，这方法有点low------------------
        im = Image.open(login_file)
        box = (737,465,837,499)   #设置要裁剪的区域(最大化时的坐标)
    #     box = (535,466,635,500)   #设置要裁剪的区域(窗口化时的坐标)
        region = im.crop(box)     #此时，region是一个新的图像对象。
    #     region.show()            #显示的话就会被占用，所以要注释掉
        region.save(login_file)
        time.sleep(1)
      
        im=Image.open(code_file)
        imgry = im.convert('L')                      #图像加强，二值化
        Brightness = ImageEnhance.Brightness(imgry)  #亮度增强，可以增加识别率
        Bright_img = Brightness.enhance(2.0)
        sharpness =ImageEnhance.Contrast(Bright_img) #对比度增强
        sharp_img = sharpness.enhance(2.0)
        
        threshold = 200                              #这个值需要根据不同的验证码进行调整，对识别率影响很大
        table = []   
        for j in range(256):        
            if j < threshold:            
                table.append(0)        
            else:            
                table.append(1)                      #使用table（是上面生成好的）生成图片    
        out = sharp_img.point(table,'1')  
        out.save(code_file)
        time.sleep(1)
        
        #调用pytesseract的识别功能
        code = self.__image_to_string(code_file)
        code = ((code.replace('\n', '')).strip()).replace(' ', '')    #去掉空格
        code = code.replace('é', '4').replace('¢', 'd').replace('$', '8').replace('»', 'v').replace('§', '2').replace('D', 'p') #对特殊情况适当替换，可根据情况调整
        code = code.lower()                          #将大写字母转为小写
        code = re.sub(r'[^A-Za-z0-9]', "", code)     #去掉非字母和数字的内容   
        if (not code):
            print u"Common: 无法识别输入源!"
            return 100101
        else:
            print u"Common: 识别结果："+code
            return code[:4]                          #截取4位验证码
        
if __name__ == '__main__':
    login_file = '//img/login_file.jpg'
    code_file = '//img/code_file.jpg'
    vcode = VCode(login_file, code_file)
    code = vcode.getCode()
    print code
