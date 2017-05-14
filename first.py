import urllib.request, urllib.parse, urllib.error
import http.cookiejar
from vcode import getVcode
from bs4 import BeautifulSoup
from prettytable import PrettyTable
from PIL import Image, ImageFilter, ImageDraw, ImageFont, ImageEnhance, ImageFilter
import os

capurl = "http://202.119.113.135/validateCodeAction.do"        # 验证码地址
posturl = "http://202.119.113.135/loginAction.do"              # 登陆地址

cookie_jar = http.cookiejar.CookieJar()
cookie_jar_handler = urllib.request.HTTPCookieProcessor(cookiejar=cookie_jar)
opener = urllib.request.build_opener(cookie_jar_handler)

picture = opener.open(capurl).read()
local = open('D:/image.jpg','wb') # 验证码写入本地project目录下验证码
local.write(picture)              # 显示验证码
local.close()

# 1. 人工识别验证码
def ManualLogin():
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36"}
    zjh = input("请输入学号：")
    mm = input("请输入密码：")
    img = Image.open('D:/image.jpg')
    img.show()
    code = input('请输入验证码：')
    os.remove('D:/image.jpg')

    postdatas = {'zjh': zjh, 'mm': mm,'v_yzm':code}
    data = urllib.parse.urlencode(postdatas).encode(encoding='gb2312')
    request = urllib.request.Request(posturl, data, headers)
    try:
        response = opener.open(request)
        html = response.read().decode('gb2312')
    except urllib.error.HTTPError as e:
        print(e.code)

# 2. 机器识别验证码，存在一定失败率
def AutomaticLogin():
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36"}
    code = getVcode()
    postdatas = {'zjh': '1506010234', 'mm': '1506010234', 'v_yzm': code}
    # 模拟登陆教务处
    data = urllib.parse.urlencode(postdatas).encode(encoding='gb2312')
    request = urllib.request.Request(posturl, data, headers)
    try:
        response = opener.open(request)
        html = response.read().decode('gb2312')
    except urllib.error.HTTPError as e:
        print(e.code)



def ManualLoginWithId(zjh):
    picture = opener.open(capurl).read()
    local = open('D:/image.jpg', 'wb')  # 验证码写入本地project目录下验证码
    local.write(picture)  # 显示验证码
    local.close()

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36"}
    # zjh = input("请输入学号：")
    # mm = input("请输入密码：")
    img = Image.open('D:/image.jpg')
    img.show()
    code = input('请输入验证码：')
    os.remove('D:/image.jpg')
    postdatas = {'zjh': zjh, 'mm': zjh, 'v_yzm': code}
    # 模拟登陆教务处
    data = urllib.parse.urlencode(postdatas).encode(encoding='gb2312')
    request = urllib.request.Request(posturl, data, headers)
    try:
        response = opener.open(request)
        html = response.read().decode('gb2312')
    except urllib.error.HTTPError as e:
        print(e.code)

    getGrades()
    getInfo()



def getGrades():
    # 获取成绩
    gradeUrl = 'http://202.119.113.135/gradeLnAllAction.do?type=ln&oper=qbinfo' \
               '&lnxndm=2016-2017%E5%AD%A6%E5%B9%B41(%E4%B8%A4%E5%AD%A6%E6%9C%9F)' \
               '#qb_2016-2017%E5%AD%A6%E5%B9%B41(%E4%B8%A4%E5%AD%A6%E6%9C%9F)'
    gradeRequest = urllib.request.Request(gradeUrl)
    responseGrade = opener.open(gradeRequest).read().decode('gb2312')

    soup = BeautifulSoup(responseGrade,'lxml')
    raw_names = soup.select('tr > td:nth-of-type(3)')
    raw_credits = soup.select('tr > td:nth-of-type(5)')
    raw_types = soup.select('tr > td:nth-of-type(6)')
    raw_grades = soup.select('td > p')

    namelist = []
    typelist = []
    creditlist = []
    gradelist = []

    for raw_name,raw_type,raw_credit,raw_grade in zip(raw_names,raw_types,raw_credits,raw_grades):
        data = [
            raw_name.get_text().strip(),
            raw_type.get_text().strip(),
            raw_credit.get_text().strip(),
            raw_grade.get_text().strip()
        ]
        if(raw_type.get_text().strip() == "必修"):
            namelist.append(data[0])
            typelist.append(data[1])
            creditlist.append(data[2])
            gradelist.append(data[3])


    # 显示成绩表
    table = PrettyTable(["课程名", "课程属性", "学分", "成绩"])
    table.align["课程名"] = "l"
    table.align["课程属性"] = "m"
    table.align["学分"] = "m"
    table.align["成绩"] = "m"
    table.padding_width = 1  # One space between column edges and contents (default)
    for everyname, everytype, everycredit, everygrade in zip(namelist, typelist, creditlist, gradelist):
        table.add_row([everyname, everytype, everycredit, everygrade])
    print(table)

    def getjd(score):
        if score=="优秀": return 5.0
        if score=="良好": return 4.5
        if score=="中等": return 3.5
        if score=="及格": return 2.5
        if score=="不及格": return 0.0
        if float(score)>=90 and float(score)<=100: return 5.0
        if float(score)>=85 and float(score)<=89: return 4.5
        if float(score)>=80 and float(score)<=84: return 4.0
        if float(score)>=75 and float(score)<=79: return 3.5
        if float(score)>=70 and float(score)<=74: return 3.0
        if float(score)>=65 and float(score)<=69: return 2.5
        if float(score)>=60 and float(score)<=65: return 2.0
        if float(score)<=59: return 0.0

    sum_sum = 0.0
    sum_credit = 0.0
    for everygrade,everycredit in zip (gradelist,creditlist):
        sum_credit = sum_credit + float(everycredit)
        sum_sum = sum_sum + getjd(everygrade)*float(everycredit)
    print("总绩点为：",end="")
    print(sum_sum/sum_credit)



def getInfo():
    xjInfoUrl = "http://202.119.113.135/xjInfoAction.do?type=ln&oper=xjxx"
    infoRequest = urllib.request.Request(xjInfoUrl)
    responseInfo = opener.open(infoRequest).read().decode('gb2312')
    # print(responseInfo)
    soup2 = BeautifulSoup(responseInfo,'lxml')
    firsts = soup2.select('td[class="fieldName"]')
    seconds = soup2.select('td[width="275"]')
    firsts.pop(3)

    everynums = []
    everynames = []
    everyids = []
    everybirths = []
    everyhomes = []
    everyadds = []
    everyyuans = []
    everyzhuanyes = []
    everynianjis = []
    everybanjis = []

    for first,second in zip(firsts,seconds):
        data = [
            first.get_text().strip(),
            second.get_text().strip()
        ]
        if (first.get_text().strip() == "学号:"):
            # everynums.append(first.get_text().strip())
            everynums.append(second.get_text().strip())
        if (first.get_text().strip() == "姓名:"):
            # everynames.append(first.get_text().strip())
            everynames.append(second.get_text().strip())
        if (first.get_text().strip() == "身份证号:"):
            # everyids.append(first.get_text().strip())
            everyids.append(second.get_text().strip())
        if (first.get_text().strip() == "出生日期:"):
            # everybirths.append(first.get_text().strip())
            everybirths.append(second.get_text().strip())
        if (first.get_text().strip() == "籍贯:"):
            # everyhomes.append(first.get_text().strip())
            everyhomes.append(second.get_text().strip())
        if (first.get_text().strip() == "通讯地址:"):
            # everyadds.append(first.get_text().strip())
            everyadds.append(second.get_text().strip())
        if (first.get_text().strip() == "系所:"):
            # everyyuans.append(first.get_text().strip())
            everyyuans.append(second.get_text().strip())
        if (first.get_text().strip() == "专业:"):
            # everyzhuanyes.append(first.get_text().strip())
            everyzhuanyes.append(second.get_text().strip())
        if (first.get_text().strip() == "年级:"):
            # everynianjis.append(first.get_text().strip())
            everynianjis.append(second.get_text().strip())
        if (first.get_text().strip() == "班级:"):
            # everybanjis.append(first.get_text().strip())
            everybanjis.append(second.get_text().strip())

    # 显示成绩表
    table = PrettyTable(["学号", "姓名", "身份证号", "出生日期", "籍贯", "通讯地址", "系所", "专业", "年级", "班级"])
    table.align["学号"] = "l"
    table.align["姓名"] = "m"
    table.align["身份证号"] = "m"
    table.align["出生日期"] = "m"
    table.align["籍贯"] = "m"
    table.align["通讯地址"] = "m"
    table.align["系所"] = "m"
    table.align["专业"] = "m"
    table.align["年级"] = "m"
    table.align["班级"] = "m"
    table.padding_width = 1  # One space between column edges and contents (default)
    for everynum,everyname,everyid,everybirth,everyhome,everyadd,everyyuan,everyzhuanye,everynianji,everybanji in \
            zip(everynums,everynames,everyids,everybirths,everyhomes,everyadds,everyyuans,everyzhuanyes,everynianjis,everybanjis):
        table.add_row([everynum,everyname,everyid,everybirth,everyhome,everyadd,everyyuan,everyzhuanye,everynianji,everybanji])
    print(table)


def getCET():
    cetUrl = "http://202.119.113.135/sljglAction.do?oper=cj"
    cetRequest = urllib.request.Request(cetUrl)
    responseInfo = opener.open(cetRequest).read().decode('gb2312')

    soup2 = BeautifulSoup(responseInfo,'lxml')
    kss = soup2.select('tr > td:nth-of-type(3)')
    rqs = soup2.select('tr > td:nth-of-type(4)')
    tls = soup2.select('tr > td:nth-of-type(8)')
    yds = soup2.select('tr > td:nth-of-type(9)')
    xzs = soup2.select('tr > td:nth-of-type(10)')
    zcjs = soup2.select('tr > td:nth-of-type(12)')

    kslist = []
    rqlist = []
    tllist = []
    ydlist = []
    xzlist = []
    zcjlist = []

    for ks,rq,tl,yd,xz,zcj in zip(kss,rqs,tls,yds,xzs,zcjs):
        data = [
            ks.get_text().strip(),
            rq.get_text().strip(),
            tl.get_text().strip(),
            yd.get_text().strip(),
            xz.get_text().strip(),
            zcj.get_text().strip(),
        ]

        kslist.append(data[0])
        rqlist.append(data[1])
        tllist.append(data[2])
        ydlist.append(data[3])
        xzlist.append(data[4])
        zcjlist.append(data[5])

    # 显示成绩表
    table = PrettyTable(["考试名称", "考试时间", "听力成绩", "阅读成绩", "写作成绩", "总成绩"])
    table.align["考试名称"] = "l"
    table.align["考试时间"] = "m"
    table.align["听力成绩"] = "m"
    table.align["阅读成绩"] = "m"
    table.align["写作成绩"] = "m"
    table.align["总成绩"] = "m"
    table.padding_width = 1  # One space between column edges and contents (default)
    for kslist,rqlist,tllist,ydlist,xzlist,zcjlist in zip(kslist,rqlist,tllist,ydlist,xzlist,zcjlist):
        table.add_row([kslist,rqlist,tllist,ydlist,xzlist,zcjlist])
    print(table)




if __name__ == '__main__':
    ManualLogin()
    getGrades()
    getCET()
