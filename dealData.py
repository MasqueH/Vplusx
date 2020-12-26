import numpy as np
import pandas as pd
import decimal as dc 

#decimal精度控制
dc.getcontext().prec = 6

#匹配map的key  取出所需的value

# 资产负债表    合并利润表    现金流量表
testMap = {"资产负债表-预付款项(元)" : ["100,2000014,566.0002","200,214,566.0002",None,"400,214,566.0002","500,214,566.0002"]
          ,"资产负债表-应收账款(元)" : ["10,214,566.0002","20,214,566.0002","30,214,566.0002","","50,214,566.0002"]
          ,"资产负债表-其他应收款(元)" : ["1,214,566.0002","2,214,566.0002","3,214,566.0002","  ","5,214,566.0002"]
          ,'资产负债表-资产合计':["1,214,566.0002","2,214,566.0002","3,214,566.0002","  ","5,214,566.0002"]
          ,'资产负债表-负债合计':["1,014,566.0002","1,214,566.0002","2,214,566.0002","  ","1,214,566.0002"]
          ,'资产负债表-应付票据及应付账款':["1,014,566.0002","1,214,566.0002","2,214,566.0002","  ","1,214,566.0002"]
          ,'资产负债表-预收账款':["1,014,566.0002","1,214,566.0002","2,214,566.0002","  ","1,214,566.0002"]
          ,'资产负债表-应收票据':["1,014,566.0002","1,214,566.0002","2,214,566.0002","  ","1,214,566.0002"]
          ,'资产负债表-应收账款':["1,014,566.0002","1,214,566.0002","2,214,566.0002","  ","1,214,566.0002"]
          ,'资产负债表-预付账款':["1,014,566.0002","1,214,566.0002","2,214,566.0002","  ","1,214,566.0002"]
          ,'资产负债表-固定资产':["1,014,566.0002","1,214,566.0002","2,214,566.0002","  ","1,214,566.0002"]
          ,'资产负债表-在建工程':["1,014,566.0002","1,214,566.0002","2,214,566.0002","  ","1,214,566.0002"]
          ,'资产负债表-工程物资':["1,014,566.0002","1,214,566.0002","2,214,566.0002","  ","1,214,566.0002"]}

#判断字符串非空
def isNotEmpty(x):
    if x is None or len(x) == 0 or len(x.strip()) == 0 :return False
    else: return True
        
    
#转换数字中的千分位
def formatString2Decimal(string):
    if isNotEmpty(string):
       return dc.Decimal(string.replace(",",""))
    else :return dc.Decimal('0.00001')

#迭代打印
def printIter(x):
    for item in x:
        print(item)

endMap = {}

v_length = len(testMap['资产负债表-资产合计'])

#对元组中数据做替换千分位的操作
for key in testMap.keys():
    endMap[key] = list(map(lambda x: formatString2Decimal(x),testMap[key]))
    
    
default_denominator = dc.Decimal(0.0001)
default_length=5
#增长率计算  
def getRate(x,v_length = default_length):
    res = [0.0]*v_length
    for i in range(v_length - 1) :            
        res[i + 1] = (x[i + 1]-x[i])/x[i]
    return res
        
print(getRate(endMap['资产负债表-资产合计']))


#负债率计算  x--> 总资产   y--> 总负债
def getDebtRate(x,y):
    if len(x) != len(y):
        raise Exception("资产和负债年份长度不匹配")  
    res = [0.0]*len(x)
    for i in range(len(x)) :
        res[i] = y[i]/x[i]
    return res
        
print(getDebtRate(endMap['资产负债表-资产合计'],endMap['资产负债表-负债合计']))

#第5步，看总资产，判断公司实力及扩张能力。（总资产看2点：一看金额，二看增长率）、
#一般来说，总资产金额大的公司实力更强，总资产同比增长快的企业扩张能力更强。
# 1.总资产 
testMap['资产负债表-资产合计']

#第6步，看资产负债率，判断公司的债务风险。资产负债率大于60%的企业，偿债风险较大，淘汰。
# 2.总负债
testMap['资产负债表-负债合计']

#第7步，看有息负债和货币资金，判断偿债风险。（看2点：1看两者大小，
#2看有无异常-比如货币资金和短期借款、长期借款金额都很大，很可能企业实际没钱）资产负债率大于40%，货币资金小于有息负债的公司，淘汰。
# 3.货币资金
# 4.短期借债
# 一年内到期的非流动负债
# 5.长期借债
# 6.长期应付款合计   
def getSolvencyRisk():


# 7.应付票据及应付账款    --> （应付票据及应付账款+预收账款）  -  （应收票据+应收账款+预付账款）
#（看2点，1看应付预收-应收预付的差额，2看应收账款占总资产的比率）应收预付金额越小，代表公司竞争力越强，行业地位越高
# 8.应付票据
# 9.应付账款
# 10.预收款项
# 11.应收票据及应收账款
# 12.应收票据
# 13.应收账款
# 14.预付款项

#无偿占用上下游资金金额：
def getFreeAmount(endMap):
    return np.array(endMap['资产负债表-应付票据及应付账款']) + np.array(endMap['资产负债表-预收账款']) -\
            np.array(endMap['资产负债表-应收票据']) - np.array(endMap['资产负债表-应收账款']) - np.array(endMap['资产负债表-预付账款'])

print(np.array(endMap['资产负债表-应付票据及应付账款']) + np.array(endMap['资产负债表-预收账款']) - \
      np.array(endMap['资产负债表-应收票据']) - np.array(endMap['资产负债表-应收账款']) - np.array(endMap['资产负债表-预付账款']))

#应收账款占总资产比例
def getDebtReceivable(endMap):
    pass
print(np.array(endMap['资产负债表-应收账款'])/np.array(endMap['资产负债表-资产合计']))


#第9步，看固定资产，判断公司的轻重。（固定资产+在建工程+工程物资）//总资产*100%>40%,属于重资产型公司，
#反之轻资产公司）重资产型公司维持竞争力的成本比较高，风险比较大，但不代表公司盈利能力差。
#固定资产
#在建工程
#工程物资

#固定资产及在建工程占总资产比率
def getFixedAssetsRate(endMap):
    pass

print(np.array(endMap['资产负债表-固定资产']) + np.array(endMap['资产负债表-在建工程']) + np.array(endMap['资产负债表-工程物资']))
print((np.array(endMap['资产负债表-固定资产']) + np.array(endMap['资产负债表-在建工程']) + np.array(endMap['资产负债表-工程物资']))/np.array(endMap['资产负债表-资产合计']))


#第10步，看投资类资产，判断公司的专注程度。优秀公司的主业无关的投资类资产很多为0，主业无关的投资类资产占总资产比率大于10%的公司淘汰掉
#以公允价值计量且其变动计入当期损益的金融资产
#可供出售金融资产
#持有至到期投资 
#投资性房地产
#长期股权投资

#与主业无关的投资
def getIndependenceInvestRate():
    pass

print(np.array(endMap['资产负债表-可供出售金融资产']) + np.array(endMap['资产负债表-投资性房地产']) +\
      np.array(endMap['资产负债表-以公允价值计量且其变动计入当期损益的金融负债']) + np.array(endMap['资产负债表-长期股权投资']))
      
      
      #第11步，把合并利润表和现金流量表各个科目看一遍，标记异常科目。(占总资产比率大于3%且增降幅度大于30%的异常科目标)

#打印异常科目
def getAbnormalSubject():
    pass

 
