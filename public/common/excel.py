#coding=utf-8
'''
Created on 2017-6-7
Last edited by whj 2017-8-30

@author: whj

'''
import datetime
import xlrd

ctype={0:"empty",1:"string",2:"number",3:"date",4:"boolean",5:"error"}

class Excel(object):
    def __init__(self, filePath):
        self.filePath = filePath
        self.workbook=xlrd.open_workbook(filename=self.filePath)

    def setFilePath(self, filePath):
        self.filePath = filePath
        self.workbook=xlrd.open_workbook(filename=self.filePath)

    def getFilePath(self):
        return self.filePath

    def getFile(self):
        return self.workbook
    '''
 	将excel中的内容转换为字符串
	注:boolean类型，true转为"1",false转为"0"
    '''
    def getDataInString(self,book,cell):
        cell_ctype=cell.ctype
        if cell_ctype==0:
            return ""
        elif cell_ctype==1:
            return cell.value
        elif cell_ctype==2:
            num_value=cell.value
            if int(num_value)==num_value:
                return str(int(cell.value))
            else:
                return str(num_value)
        elif cell_ctype==3:
            date_value=xlrd.xldate_as_tuple(cell.value,book.datemode)
            if(date_value[3:])==(0,0,0):
                return datetime.date(*date_value[:3]).strftime("%Y-%m-%d")
            else:
                return datetime.datetime(*date_value).strftime("%Y-%m-%d %H:%M:%S")
        elif cell_ctype==4:
            return str(cell.value)
        elif cell_ctype==5:
            return ""
        else:
            return str(cell.value)

    '''
	 读取某一sheet页,某行数据
	参数：sheet页名称,行索引(从0开始),列开始索引(从0开始),数据长度
    '''
    def getDatasByRow(self, sheetName, rowNum, sNum, length):
        book = self.workbook
        #sheetName=sheetName.decode('utf-8')
        try:
            sheet = book.sheet_by_name(sheetName)
        except:
            print "no sheet in %s named %s" % (self.filePath, sheetName)
            return
        dataList=[]
        maxLen=sheet.row(rowNum).__len__()
        for i in range(sNum,sNum+length):
            if(i<=maxLen-1):
                cellOri=sheet.cell(rowNum,i)
                if(cellOri.ctype==5):
                    print "cell(%d,%d) in sheet(%s) in file(%s) is error" % rowNum,i,sheetName,self.filePath
                    dataList.append("")
                else:
                    dataList.append(self.getDataInString(book,cellOri))
            else:
                dataList.append("")
        return dataList

    '''
	读取某一sheet页,某列数据
	参数：sheet页名称(从0开始),列索引(从0开始),行开始索引(从0开始),数据长度
    '''
    def getDatasByCol(self,sheetName,colNum,sNum,length):
        book = self.workbook
        #sheetName=sheetName.decode('utf-8')
        try:
            sheet = book.sheet_by_name(sheetName)
        except:
            print "no sheet in %s named %s" % (self.filePath, sheetName)
            return
        dataList=[]
        maxLen=sheet.col(colNum).__len__()
        for i in range(sNum,sNum+length):
            if(i<=maxLen-1):
                cellOri=sheet.cell(i,colNum)
                if(cellOri.ctype==5):
                    print "cell(%d,%d) in sheet(%s) in file(%s) is error" % (i,colNum,sheetName,self.filePath)
                    dataList.append("")
                else:
                    dataList.append(self.getDataInString(book,cellOri))
            else:
                dataList.append("")
        return dataList

    '''
	从某列中找到第一个满足的字符串，返回列序号
    '''
    def getIndexByCol(self,sheetName,colNum,dist):
        book = self.workbook
        try:
            sheet = book.sheet_by_name(sheetName)
        except:
            print "no sheet in %s named %s" % (self.filePath, sheetName)
            return 9999  #9999表示有误或没有找到
        size=sheet.col(colNum).__len__()
        for i in range(0,size):
            cellStr=self.getDataInString(book,sheet.cell(i,colNum))
            if(cellStr==dist):
                return i
            else:
                continue
        return 9999 #9999表示有误或没有找到


    '''
	从某行中找到第一个满足的字符串，返回列序号
    '''
    def getIndexByRow(self,sheetName,rowNum,dist):
        book = self.workbook
        try:
            sheet = book.sheet_by_name(sheetName)
        except:
            print "no sheet in %s named %s" % (self.filePath, sheetName)
            return 9999  #9999表示有误或没有找到
        size=sheet.row(rowNum).__len__()
        for i in range(0,size):
            cellStr=self.getDataInString(book,sheet.cell(rowNum,i))
            if(cellStr==dist):
                return i
            else:
                continue
        return 9999 #9999表示有误或没有找到
       

    '''
	 读取某一sheet页,某些行数据
	参数：sheet页索引(从0开始),行索引(从0开始),数据长度
	'''
    def getDatasBySheetIndex(self,sheetNum=0,rowNum=0,length=0):
        '''
		sheetNum：sheet序号，从0开始  
		rowNum：表头所在行，即开始读取的行号，从0开始
		length：读取的行数
		例如：
		listdata1 = Excel.getDatasBySheetIndex(0,0,4)  #读取第1个sheet中第1条开始的4条数据
		读取excel表结果为dict，结果格式是：
		[{u'username': '13984303588', u'': u'', u'password': u'w123456', u'type': u'\u6b63\u5e38'}, {u'username': u'admin', u'': u'', u'password': u'123456', u'type': u'\u6b63\u5e38'}, {u'username': u'admin', u'': u'', u'password': u'888888', u'type': u'\u5bc6\u7801\u9519\u8bef'}]
	    '''
    
        book = self.workbook
        table = book.sheets()[sheetNum]
        if length == 0:
            length = table.nrows #行数  
        colnames = table.row_values(rowNum) #某一行数据           
        datalist = []
        for rownum in range((rowNum + 1),rowNum + length):
            row = table.row_values(rownum)
            if row:
                app = {}
                for i in range(len(colnames)):
                    try:
                        #处理从excel读取的数据内容转换为字符串
                        cellOri=table.cell(rownum,i)
                        row[i] = self.getDataInString(book,cellOri)
                    except Exception,e:
                        print str(e)  
                    app[colnames[i]] = row[i]               
            datalist.append(app) 
        return datalist

    '''
             读取某一sheet页所有数据
             参数：sheet名称
    '''
    def getAllDatasBySheetName(self,sheetName):
        """
		读取excel表所有数据的结果为dict
		return [{'title':'1','user':'root'},{'title':'2','user':'xiaoshitou'}]
		"""        
#         book = self.workbook
#         table = book.sheet_by_name(sheetName)
#         dataresult = [table.row_values(i) for i in range(0, table.nrows)]
#         
#         datalist = [ dict(zip(dataresult[0], dataresult[i])) for i in range(1, len(dataresult))]
#         return datalist
        book = self.workbook
        #sheetName=sheetName.decode('utf-8')
        try:
            sheet = book.sheet_by_name(sheetName)
        except:
            print "no sheet in %s named %s" % (self.filePath, sheetName)
            return
        dataList=[]
        colnames = sheet.row_values(0) #第一行数据
        nrows=sheet.nrows
        ncols=sheet.ncols
        for i in range(1,nrows):
            row = sheet.row_values(i)
            app = {}
            if row:
                for j in range(0,ncols):
                    cellOri=sheet.cell(i,j)
                    if(cellOri.ctype==5):
                        print "cell(%d,%d) in sheet(%s) in file(%s) is error" % 0,i,sheetName,self.filePath
                        row[j] = ""
                    else:
                        row[j] = self.getDataInString(book,cellOri)
                    app[colnames[j]] = row[j]               
            dataList.append(app)
        return dataList
    '''
             读取某一sheet页所有数据
             参数：sheet索引序号
    '''
    def getAllDatasBySheetIndex(self,sheetNum):
        """
                            读取excel表所有数据的结果为dict
        return [{'title':'1','user':'root'},{'title':'2','user':'xiaoshitou'}]
        """
#         book = self.workbook
#         table = book.sheets()[sheetNum]
#         dataresult = [table.row_values(i) for i in range(0, table.nrows)]
#         
#         datalist = [ dict(zip(dataresult[0], dataresult[i])) for i in range(1, len(dataresult))]
#         return datalist
        book = self.workbook
        #sheetName=sheetName.decode('utf-8')
        try:
            sheet = book.sheets()[sheetNum]
        except:
            print "no sheet in %s named %s" % (self.filePath, sheetNum)
            return
        dataList=[]
        colnames = sheet.row_values(0) #第一行数据
        nrows=sheet.nrows
        ncols=sheet.ncols
        for i in range(1,nrows):
            row = sheet.row_values(i)
            app = {}
            if row:
                for j in range(0,ncols):
                    cellOri=sheet.cell(i,j)
                    if(cellOri.ctype==5):
                        print "cell(%d,%d) in sheet(%s) in file(%s) is error" % 0,i,sheetNum,self.filePath
                        row[j] = ""
                    else:
                        row[j] = self.getDataInString(book,cellOri)
                    app[colnames[j]] = row[j]               
            dataList.append(app)
        return dataList

# 	def get_url_data(title):
# 		"""
# 		读取txt文件，转化成dict;读取url和导航栏的对应关系
# 		将txt转化成一个字典:下单=>/admin/order/index
# 		{'title1':'url1','下单':'/admin/order/index'}
# 		"""
# 		name = 'urlsource.txt'
# 		txtpath = os.path.join(data_path,name)
# 		with codecs.open(txtpath,'r',encoding='utf-8') as f:
# 			xtcontent = f.readlines()
# 		txtdict = dict([txt.strip().replace('\ufeff','').split('=>') for txt in txtcontent])
# 		return txtdict[title]

    def closeExcel(self):
        self.workbook=None

############################################################以下是对excel中指定格式数据解析，暂时未使用#####################################
#     '''
#     读取指定格式的datas，完成指定操作
#     datas格式要求如下：
#     datas=[
#         {"xpath":"","op":"get","value":""},
#         {"xpath":"//input[@id='logonInfo.logUserName']","op":"sendKeys","value":"dongfang"}
#     ]
#     '''
#     def fixTheForm(self, title,datas,logDir=None,filePath=None,defaultParams=None):
#         params={}
#         if(defaultParams <> None and defaultParams.__len__()>0):
#             for (k,v) in defaultParams.items():
#                 params.__setitem__(k,v)
#                 
#         result = {"state": True, "info": self.getNowStrftime(),"title":">>>"+title}
#         for i in range(datas.__len__()):
#             tmp = datas.__getitem__(i)
#             _op=tmp.get("op").lower()
#             _xpath=tmp.get("xpath")
#             _value=tmp.get("value")
#             if(_op=="skip"):
#                 continue
#             
#             #处理保存参数操作,value是个有返回值的js语句
#             pattern1=re.compile(r"\{@(\w+)@\}")
#             m1=pattern1.match(_op)
#             if(m1):
#                 try:
#                     ret=str(self.driver.execute_script(_value))
#                     self.driver.implicitly_wait(2)
#                     params.__setitem__(m1.group(1),ret)
#                     t_result = {"state": True, "info": ""}
#                     result = self.mergeResult(result,t_result)
#                     continue
#                 except Exception as e:
#                     t_result = {"state": False, "info": getErrInfo(_xpath,"executeJs",_value,str(e))}
#                     result = self.mergeResult(result,t_result)
#                     continue
# 
#             #print params
# 
#             #处理带参数的xpath
#             if (_xpath.__contains__(self.XPATHARG) and _value.__contains__(self.SPLITMARK)):
#                 indx = _value.find(self.SPLITMARK)
#                 xpathParm = _value[:indx]
#                 _xpath = _xpath.replace(self.XPATHARG,xpathParm)
#                 _value = _value[indx + self.SPLITMARK.__len__():]
# 
#             #处理value中含有参数
#             pattern2=re.compile(r".*\{@(\w+)@\}.*")
#             c=0
#             while pattern2.match(_value) and c<100:  #防止无限循环
#                 m2=pattern2.match(_value)
#                 t_key=m2.group(1)
#                 c=c+1
#                 if(params.has_key(t_key)):
#                     _value=_value.replace("{@"+t_key+"@}",params.get(t_key))
#                 else:
#                     _value==_value.replace("{@"+t_key+"@}","{"+t_key+"}")
# 
#             #处理调用公共步骤
#             if(_op=="call" and filePath<>None):
#                 dParams={}
#                 tValues=_value.split(self.SPLITMARK)
#                 if(tValues.__len__()>1):
#                     for i in range(1,tValues.__len__()):
#                         tParamValue=tValues[i].split("=")
#                         dParams.__setitem__(tParamValue[0],tParamValue[1])
#                 t_result=self.runSteps(filePath,tValues[0],None,dParams).__getitem__(0)
#                 t_result.__setitem__("info",u"第"+str(i+1)+u"步调用公共步骤"+_value+":"+t_result.get("info"))
#                 result = self.mergeResult(result,t_result)
#                 continue
# 
#             #处理上传\比较下载文件操作的相对链接
#             if((_op=="upload" or _op=="sameaslocalfile") and (not _value.__contains__(":"))):
#                 if(logDir<>None):
#                     _value=os.path.join(os.path.dirname(logDir),_value)
#                 else:
#                     print "can't find the logs dir,can't use the relative path"
# 
# 
#             #处理正常操作
#             t_result = self.doOperate(_op,_xpath,_value)
#             if(not t_result.get("state")):
#                 if((_xpath or "").__len__()>0 and
#                        BrowserManage.isElementPresent(self.driver,By.XPATH,_xpath)):
#                     BrowserManage.scrollToElement(self.driver,self.driver.find_element_by_xpath(_xpath))
#                 if(logDir<>None):
#                     snapFile=os.path.join(logDir,self.getNowStrftime2()+".png")
#                     self.driver.get_screenshot_as_file(snapFile)
#                     snapInfo="<img src=\"file:\\\\\\"+os.path.abspath(snapFile).strip()+"\" height=\"600\" width=\"800\">"
#                 else:
#                     print "can't find the logs dir,can't use the relative path"
#                     snapInfo=""
#                 t_result.__setitem__("info",u"第"+str(i+1)+u"步:"+t_result.get("info")+u"\n截图:\n"+snapInfo+"\n")
#                 result = self.mergeResult(result,t_result)
#         if(result.get("state")):
#             result.__setitem__("info",result.get("info")+" PASS\n")
#         return result
# 
#     '''
#     解析指定格式数据，将其解析成fixTheForm需要的数据
#     originDatas的格式(元素名称)如下：
#     '''
#     def parseDatasFromStdExcel(self,filePath,sheetName):
#         em=Excel(filePath)
#         dataStepSize=int(em.getDatasByCol(sheetName,1,0,1)[0])
#         dataGroupSize=int(em.getDatasByCol(sheetName,2,0,1)[0])
#         xpath_array=self.getXpathArrayFromStdExcel(filePath,sheetName,dataStepSize)
#         datas=[]
#         i=0
#         while(i<dataGroupSize):
#             piece=None
#             runState=self.YES
#             title=""
#             isRun=em.getDatasByCol(sheetName,3+2*i,0,1)[0]
#             if( isRun==u"忽略" or isRun==""):
#                 runState=self.NO
#             title=em.getDatasByCol(sheetName,4+2*i,0,1)[0]
#             op_array=em.getDatasByCol(sheetName,3+2*i,2,dataStepSize)
#             value_array=em.getDatasByCol(sheetName,4+2*i,2,dataStepSize)
#             piece=(runState,title,self.mergeInputDatas(xpath_array,op_array,value_array))
#             datas.append(piece)
#             i=i+1
#         em.closeExcel()
#         return datas
# 
#     '''
#     获取xpathArray
#     '''
#     def getXpathArrayFromStdExcel(self,filePath,sheetName,dataSize):
#         em=Excel(filePath)
#         sheetNames=em.getDatasByCol(sheetName,1,2,dataSize)
#         elementNames=em.getDatasByCol(sheetName,2,2,dataSize)
#         xpath_array=[]
#         for i in range(0,dataSize):
#             t_sheetName=sheetNames[i].strip()
#             t_elementName=elementNames[i].strip()
#             if(t_sheetName=="" or t_elementName==""):
#                 xpath_array.append("")
#                 continue
#             else:
#                 idx=em.getIndexByCol(t_sheetName,1,t_elementName)
#                 if(idx>9000):
#                     raise ValueError,"The (%d)st row in sheet(%s) of file(%s) has ERROR" % (i,sheetName,filePath)
#                 xpath_array.append(em.getDatasByCol(t_sheetName,2,idx,1)[0])
#                 continue
#         return xpath_array
# 
# 
#     '''
#     合并xpath数组，操作数组，值数组.
#     构成字典列表
#     '''
#     def mergeInputDatas(self,xpath_array,op_array,value_array):
#         length=xpath_array.__len__()
#         inputDatas=[]
#         for i in range(0,length):
#             t_op=""
#             t_value=""
#             if(i>=op_array.__len__()):
#                 t_op=""
#             else:
#                 t_op=op_array[i]
#             if(i>=value_array.__len__()):
#                 t_value=""
#             else:
#                 t_value=value_array[i]
#             inputDatas.append({"xpath":xpath_array[i],"op":t_op,"value":t_value})
#         return inputDatas
# 
#     '''
#     获取当前时间的格式化字符串
#     '''
#     def getNowStrftime(self):
#         return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     def getNowStrftime2(self):
#         return datetime.datetime.now().strftime("%Y%m%d%H%M%S")
# 
#     '''
#     合并各个步骤的测试结果
#     '''
#     def mergeResult(self,result,t_result):
#         result.__setitem__("state",result.get("state") and t_result.get("state"))
#         result.__setitem__("info",result.get("info")+"\n"+t_result.get("info"))
#         return result
# 
#     '''
#     运行指定格式sheet页中的测试用例
#     '''
#     def runCase(self,filePath,sheetName,logsDir=None):
#         datas=self.parseDatasFromStdExcel(filePath,sheetName)
#         resultList=[]
#         for i in range(0,datas.__len__()):
#             piece=datas.__getitem__(i)
#             runState=piece[0]
#             if(runState==self.NO):
#                 continue
#             else:
#                 title=piece[1]
#                 inputDatas=piece[2]
#             t_result=self.fixTheForm(title,inputDatas,logDir=logsDir,filePath=filePath)
#             resultList.append(t_result)
#         return resultList
# 
# 
#     '''
#     运行指定格式sheet页中的测试用例
#     '''
#     def runSteps(self,filePath,sheetName,logsDir=None,dParams=None):
#         datas=self.parseDatasFromStdExcel(filePath,sheetName)
#         resultList=[]
#         for i in range(0,datas.__len__()):
#             piece=datas.__getitem__(i)
#             runState=piece[0]
#             if(runState==self.NO):
#                 continue
#             else:
#                 title=piece[1]
#                 inputDatas=piece[2]
#             t_result=self.fixTheForm(title,inputDatas,logDir=logsDir,filePath=filePath,defaultParams=dParams)
#             resultList.append(t_result)
#         return resultList
# 
#     '''
#     获取指定格式excel中的测试集
#     '''
#     @staticmethod
#     def getTestSuiteFromStdExcel(filePath):
#         em=Excel(filePath)
#         caseCount=int(em.getDatasByCol(u'配置',3,0,1)[0])
#         caseArray=em.getDatasByCol(u"配置",2,2,caseCount)
#         stateArray=em.getDatasByCol(u"配置",3,2,caseCount)
#         runCaseList=[]
#         for i in range(0,caseCount):
#             if(stateArray[i]<>u"忽略"):
#                 runCaseList.append(caseArray[i])
#         return runCaseList


if "__main__" == __name__:
    '''
    s=(1992, 2, 22,22, 1, 33)
    print s[:3]
    print s[3:]
    print str(datetime.datetime(*s[:3]))
    print datetime.datetime(*s).strftime("%Y-%m-%d %H:%M:%S")
   '''
    file=r"E:\workspace\TestPySeUI\data\testdata\case.xls"
    print file
    em=Excel(file)
#     print em.getDatasByCol(u"CASE_搜索关键词",3,1,5)
#     print (em.getDatasByCol(u"CASE_搜索关键词",3,1,5)[0]==u"元素XPATH(此列拖拽后不要清除)")
#     print em.getDatasByRow(u"DDD",1,3,3)
#     print em.getDatasByRow(u"CASE_搜索关键词",2,1,5)
    print em.getDatasBySheetIndex(0,0,14)  
    print em.getAllDatasBySheetName(u"Login")
    print em.getAllDatasBySheetIndex(0)


