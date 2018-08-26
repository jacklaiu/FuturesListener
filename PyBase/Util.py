import tushare as ts
import time
import datetime
import requests
import threading

exchange_code_rel = {

    'SHFE': ['RU', 'RB', 'BU', 'HC'],

    'CZCE': ['A', 'B', 'M', 'J', 'JM', 'C', 'Y', 'L', 'PP', 'V', 'P', 'JD', 'I', 'FB', 'CS'],

    'DCE': ['AP', 'FG', 'MA', 'SF', 'SM', 'CF', 'SR', 'OI', 'RM', 'TA', 'ZC']

}

class Async_req(threading.Thread):
    def __init__(self, url):
        threading.Thread.__init__(self)
        self.url = url
    def run(self):
        requests.get(self.url)

def timeDur_ReturnSec(startTime, endTime):
    startTime = datetime.datetime.strptime(startTime, "%Y-%m-%d %H:%M:%S")
    endTime = datetime.datetime.strptime(endTime, "%Y-%m-%d %H:%M:%S")
    # 相减得到秒数
    seconds = (endTime - startTime).seconds
    return seconds

def getExchange(kind):
    for key in exchange_code_rel.keys():
        kinds = exchange_code_rel[key]
        if kind in kinds:
            return key
    return None

def isOpenTime_wide():
    for ex in exchange_code_rel.keys():
        isopen = isOpenTime(ex)
        if isopen is True:
            return True
    return False

def isOpenTime_Kind(kind):
    if kind is None:
        return False
    return isOpenTime(getExchange(kind))

def isOpenTime(exchange):
    if exchange is None:
        return False
    exchange = exchange.lower()
    if isTodayOpen() is False:
        return False
    now = getHMS()
    if exchange is "shfe" and '09:00:00' < now < '10:15:00' and '10:30:00' < now < '11:30:00' and '13:30:00' < now < '15:00:00' and '21:00:00' < now < '23:00:00':
        return True
    if exchange is "czce" and '09:00:00' < now < '10:15:00' and '10:30:00' < now < '11:30:00' and '13:30:00' < now < '15:00:00' and '21:00:00' < now < '23:30:00':
        return True
    if exchange is "dce" and '09:00:00' < now < '10:15:00' and '10:30:00' < now < '11:30:00' and '13:30:00' < now < '15:00:00' and '21:00:00' < now < '23:30:00':
        return True
    return False

def isTodayOpen():
    return isOpen(getYMD())

def getYMDHMS():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

def getYMD():
    return time.strftime("%Y-%m-%d", time.localtime())

def getHMS():
    return time.strftime("%H:%M:%S", time.localtime())

def getTimeStamp():
    millis = int(round(time.time() * 1000))
    return millis

def getFormatToday():
    return time.strftime("%Y-%m-%d", time.localtime())

def getPreDayYMD(num=1, startdate=None):
    today=datetime.date.today()
    if startdate is not None:
        arr = startdate.split("-")
        today = datetime.date(int(arr[0]), int(arr[1]), int(arr[2]))
    oneday=datetime.timedelta(days=num)
    d=today-oneday
    return str(d)

def get_concept_securities():
    df = ts.get_concept_classified()
    values = df.values
    concept_code_dict = {}
    for row in values:
        code = row[0]
        c_name = row[2]
        if c_name not in concept_code_dict:
            concept_code_dict.setdefault(c_name, [code])
        else:
            concept_code_dict[c_name].append(code)
    return concept_code_dict


def initOpenDateTempFile():
    OpenList = ts.trade_cal()
    rows = OpenList[OpenList.isOpen == 1].values[-888:]
    f = open("../temp_OpenDate.txt", "w")
    f.write("")
    f.close()
    f = open("temp_OpenDate.txt", "a")
    for row in rows:
        date = row[0]
        f.write(date + ";")
    f.close()

def getOpenDates():
    #f = open(os.path.dirname(__file__) + "/temp_OpenDate.txt", "r")
    #str = f.read()
    str = "2015-05-18;2015-05-19;2015-05-20;2015-05-21;2015-05-22;2015-05-25;2015-05-26;2015-05-27;2015-05-28;2015-05-29;2015-06-01;2015-06-02;2015-06-03;2015-06-04;2015-06-05;2015-06-08;2015-06-09;2015-06-10;2015-06-11;2015-06-12;2015-06-15;2015-06-16;2015-06-17;2015-06-18;2015-06-19;2015-06-23;2015-06-24;2015-06-25;2015-06-26;2015-06-29;2015-06-30;2015-07-01;2015-07-02;2015-07-03;2015-07-06;2015-07-07;2015-07-08;2015-07-09;2015-07-10;2015-07-13;2015-07-14;2015-07-15;2015-07-16;2015-07-17;2015-07-20;2015-07-21;2015-07-22;2015-07-23;2015-07-24;2015-07-27;2015-07-28;2015-07-29;2015-07-30;2015-07-31;2015-08-03;2015-08-04;2015-08-05;2015-08-06;2015-08-07;2015-08-10;2015-08-11;2015-08-12;2015-08-13;2015-08-14;2015-08-17;2015-08-18;2015-08-19;2015-08-20;2015-08-21;2015-08-24;2015-08-25;2015-08-26;2015-08-27;2015-08-28;2015-08-31;2015-09-01;2015-09-02;2015-09-07;2015-09-08;2015-09-09;2015-09-10;2015-09-11;2015-09-14;2015-09-15;2015-09-16;2015-09-17;2015-09-18;2015-09-21;2015-09-22;2015-09-23;2015-09-24;2015-09-25;2015-09-28;2015-09-29;2015-09-30;2015-10-08;2015-10-09;2015-10-12;2015-10-13;2015-10-14;2015-10-15;2015-10-16;2015-10-19;2015-10-20;2015-10-21;2015-10-22;2015-10-23;2015-10-26;2015-10-27;2015-10-28;2015-10-29;2015-10-30;2015-11-02;2015-11-03;2015-11-04;2015-11-05;2015-11-06;2015-11-09;2015-11-10;2015-11-11;2015-11-12;2015-11-13;2015-11-16;2015-11-17;2015-11-18;2015-11-19;2015-11-20;2015-11-23;2015-11-24;2015-11-25;2015-11-26;2015-11-27;2015-11-30;2015-12-01;2015-12-02;2015-12-03;2015-12-04;2015-12-07;2015-12-08;2015-12-09;2015-12-10;2015-12-11;2015-12-14;2015-12-15;2015-12-16;2015-12-17;2015-12-18;2015-12-21;2015-12-22;2015-12-23;2015-12-24;2015-12-25;2015-12-28;2015-12-29;2015-12-30;2015-12-31;2016-01-04;2016-01-05;2016-01-06;2016-01-07;2016-01-08;2016-01-11;2016-01-12;2016-01-13;2016-01-14;2016-01-15;2016-01-18;2016-01-19;2016-01-20;2016-01-21;2016-01-22;2016-01-25;2016-01-26;2016-01-27;2016-01-28;2016-01-29;2016-02-01;2016-02-02;2016-02-03;2016-02-04;2016-02-05;2016-02-15;2016-02-16;2016-02-17;2016-02-18;2016-02-19;2016-02-22;2016-02-23;2016-02-24;2016-02-25;2016-02-26;2016-02-29;2016-03-01;2016-03-02;2016-03-03;2016-03-04;2016-03-07;2016-03-08;2016-03-09;2016-03-10;2016-03-11;2016-03-14;2016-03-15;2016-03-16;2016-03-17;2016-03-18;2016-03-21;2016-03-22;2016-03-23;2016-03-24;2016-03-25;2016-03-28;2016-03-29;2016-03-30;2016-03-31;2016-04-01;2016-04-05;2016-04-06;2016-04-07;2016-04-08;2016-04-11;2016-04-12;2016-04-13;2016-04-14;2016-04-15;2016-04-18;2016-04-19;2016-04-20;2016-04-21;2016-04-22;2016-04-25;2016-04-26;2016-04-27;2016-04-28;2016-04-29;2016-05-03;2016-05-04;2016-05-05;2016-05-06;2016-05-09;2016-05-10;2016-05-11;2016-05-12;2016-05-13;2016-05-16;2016-05-17;2016-05-18;2016-05-19;2016-05-20;2016-05-23;2016-05-24;2016-05-25;2016-05-26;2016-05-27;2016-05-30;2016-05-31;2016-06-01;2016-06-02;2016-06-03;2016-06-06;2016-06-07;2016-06-08;2016-06-13;2016-06-14;2016-06-15;2016-06-16;2016-06-17;2016-06-20;2016-06-21;2016-06-22;2016-06-23;2016-06-24;2016-06-27;2016-06-28;2016-06-29;2016-06-30;2016-07-01;2016-07-04;2016-07-05;2016-07-06;2016-07-07;2016-07-08;2016-07-11;2016-07-12;2016-07-13;2016-07-14;2016-07-15;2016-07-18;2016-07-19;2016-07-20;2016-07-21;2016-07-22;2016-07-25;2016-07-26;2016-07-27;2016-07-28;2016-07-29;2016-08-01;2016-08-02;2016-08-03;2016-08-04;2016-08-05;2016-08-08;2016-08-09;2016-08-10;2016-08-11;2016-08-12;2016-08-15;2016-08-16;2016-08-17;2016-08-18;2016-08-19;2016-08-22;2016-08-23;2016-08-24;2016-08-25;2016-08-26;2016-08-29;2016-08-30;2016-08-31;2016-09-01;2016-09-02;2016-09-05;2016-09-06;2016-09-07;2016-09-08;2016-09-09;2016-09-12;2016-09-13;2016-09-14;2016-09-19;2016-09-20;2016-09-21;2016-09-22;2016-09-23;2016-09-26;2016-09-27;2016-09-28;2016-09-29;2016-09-30;2016-10-10;2016-10-11;2016-10-12;2016-10-13;2016-10-14;2016-10-17;2016-10-18;2016-10-19;2016-10-20;2016-10-21;2016-10-24;2016-10-25;2016-10-26;2016-10-27;2016-10-28;2016-10-31;2016-11-01;2016-11-02;2016-11-03;2016-11-04;2016-11-07;2016-11-08;2016-11-09;2016-11-10;2016-11-11;2016-11-14;2016-11-15;2016-11-16;2016-11-17;2016-11-18;2016-11-21;2016-11-22;2016-11-23;2016-11-24;2016-11-25;2016-11-28;2016-11-29;2016-11-30;2016-12-01;2016-12-02;2016-12-05;2016-12-06;2016-12-07;2016-12-08;2016-12-09;2016-12-12;2016-12-13;2016-12-14;2016-12-15;2016-12-16;2016-12-19;2016-12-20;2016-12-21;2016-12-22;2016-12-23;2016-12-26;2016-12-27;2016-12-28;2016-12-29;2016-12-30;2017-01-03;2017-01-04;2017-01-05;2017-01-06;2017-01-09;2017-01-10;2017-01-11;2017-01-12;2017-01-13;2017-01-16;2017-01-17;2017-01-18;2017-01-19;2017-01-20;2017-01-23;2017-01-24;2017-01-25;2017-01-26;2017-02-03;2017-02-06;2017-02-07;2017-02-08;2017-02-09;2017-02-10;2017-02-13;2017-02-14;2017-02-15;2017-02-16;2017-02-17;2017-02-20;2017-02-21;2017-02-22;2017-02-23;2017-02-24;2017-02-27;2017-02-28;2017-03-01;2017-03-02;2017-03-03;2017-03-06;2017-03-07;2017-03-08;2017-03-09;2017-03-10;2017-03-13;2017-03-14;2017-03-15;2017-03-16;2017-03-17;2017-03-20;2017-03-21;2017-03-22;2017-03-23;2017-03-24;2017-03-27;2017-03-28;2017-03-29;2017-03-30;2017-03-31;2017-04-05;2017-04-06;2017-04-07;2017-04-10;2017-04-11;2017-04-12;2017-04-13;2017-04-14;2017-04-17;2017-04-18;2017-04-19;2017-04-20;2017-04-21;2017-04-24;2017-04-25;2017-04-26;2017-04-27;2017-04-28;2017-05-02;2017-05-03;2017-05-04;2017-05-05;2017-05-08;2017-05-09;2017-05-10;2017-05-11;2017-05-12;2017-05-15;2017-05-16;2017-05-17;2017-05-18;2017-05-19;2017-05-22;2017-05-23;2017-05-24;2017-05-25;2017-05-26;2017-05-31;2017-06-01;2017-06-02;2017-06-05;2017-06-06;2017-06-07;2017-06-08;2017-06-09;2017-06-12;2017-06-13;2017-06-14;2017-06-15;2017-06-16;2017-06-19;2017-06-20;2017-06-21;2017-06-22;2017-06-23;2017-06-26;2017-06-27;2017-06-28;2017-06-29;2017-06-30;2017-07-03;2017-07-04;2017-07-05;2017-07-06;2017-07-07;2017-07-10;2017-07-11;2017-07-12;2017-07-13;2017-07-14;2017-07-17;2017-07-18;2017-07-19;2017-07-20;2017-07-21;2017-07-24;2017-07-25;2017-07-26;2017-07-27;2017-07-28;2017-07-31;2017-08-01;2017-08-02;2017-08-03;2017-08-04;2017-08-07;2017-08-08;2017-08-09;2017-08-10;2017-08-11;2017-08-14;2017-08-15;2017-08-16;2017-08-17;2017-08-18;2017-08-21;2017-08-22;2017-08-23;2017-08-24;2017-08-25;2017-08-28;2017-08-29;2017-08-30;2017-08-31;2017-09-01;2017-09-04;2017-09-05;2017-09-06;2017-09-07;2017-09-08;2017-09-11;2017-09-12;2017-09-13;2017-09-14;2017-09-15;2017-09-18;2017-09-19;2017-09-20;2017-09-21;2017-09-22;2017-09-25;2017-09-26;2017-09-27;2017-09-28;2017-09-29;2017-10-09;2017-10-10;2017-10-11;2017-10-12;2017-10-13;2017-10-16;2017-10-17;2017-10-18;2017-10-19;2017-10-20;2017-10-23;2017-10-24;2017-10-25;2017-10-26;2017-10-27;2017-10-30;2017-10-31;2017-11-01;2017-11-02;2017-11-03;2017-11-06;2017-11-07;2017-11-08;2017-11-09;2017-11-10;2017-11-13;2017-11-14;2017-11-15;2017-11-16;2017-11-17;2017-11-20;2017-11-21;2017-11-22;2017-11-23;2017-11-24;2017-11-27;2017-11-28;2017-11-29;2017-11-30;2017-12-01;2017-12-04;2017-12-05;2017-12-06;2017-12-07;2017-12-08;2017-12-11;2017-12-12;2017-12-13;2017-12-14;2017-12-15;2017-12-18;2017-12-19;2017-12-20;2017-12-21;2017-12-22;2017-12-25;2017-12-26;2017-12-27;2017-12-28;2017-12-29;2018-01-02;2018-01-03;2018-01-04;2018-01-05;2018-01-08;2018-01-09;2018-01-10;2018-01-11;2018-01-12;2018-01-15;2018-01-16;2018-01-17;2018-01-18;2018-01-19;2018-01-22;2018-01-23;2018-01-24;2018-01-25;2018-01-26;2018-01-29;2018-01-30;2018-01-31;2018-02-01;2018-02-02;2018-02-05;2018-02-06;2018-02-07;2018-02-08;2018-02-09;2018-02-12;2018-02-13;2018-02-14;2018-02-22;2018-02-23;2018-02-26;2018-02-27;2018-02-28;2018-03-01;2018-03-02;2018-03-05;2018-03-06;2018-03-07;2018-03-08;2018-03-09;2018-03-12;2018-03-13;2018-03-14;2018-03-15;2018-03-16;2018-03-19;2018-03-20;2018-03-21;2018-03-22;2018-03-23;2018-03-26;2018-03-27;2018-03-28;2018-03-29;2018-03-30;2018-04-02;2018-04-03;2018-04-04;2018-04-09;2018-04-10;2018-04-11;2018-04-12;2018-04-13;2018-04-16;2018-04-17;2018-04-18;2018-04-19;2018-04-20;2018-04-23;2018-04-24;2018-04-25;2018-04-26;2018-04-27;2018-05-02;2018-05-03;2018-05-04;2018-05-07;2018-05-08;2018-05-09;2018-05-10;2018-05-11;2018-05-14;2018-05-15;2018-05-16;2018-05-17;2018-05-18;2018-05-21;2018-05-22;2018-05-23;2018-05-24;2018-05-25;2018-05-28;2018-05-29;2018-05-30;2018-05-31;2018-06-01;2018-06-04;2018-06-05;2018-06-06;2018-06-07;2018-06-08;2018-06-11;2018-06-12;2018-06-13;2018-06-14;2018-06-15;2018-06-19;2018-06-20;2018-06-21;2018-06-22;2018-06-25;2018-06-26;2018-06-27;2018-06-28;2018-06-29;2018-07-02;2018-07-03;2018-07-04;2018-07-05;2018-07-06;2018-07-09;2018-07-10;2018-07-11;2018-07-12;2018-07-13;2018-07-16;2018-07-17;2018-07-18;2018-07-19;2018-07-20;2018-07-23;2018-07-24;2018-07-25;2018-07-26;2018-07-27;2018-07-30;2018-07-31;2018-08-01;2018-08-02;2018-08-03;2018-08-06;2018-08-07;2018-08-08;2018-08-09;2018-08-10;2018-08-13;2018-08-14;2018-08-15;2018-08-16;2018-08-17;2018-08-20;2018-08-21;2018-08-22;2018-08-23;2018-08-24;2018-08-27;2018-08-28;2018-08-29;2018-08-30;2018-08-31;2018-09-03;2018-09-04;2018-09-05;2018-09-06;2018-09-07;2018-09-10;2018-09-11;2018-09-12;2018-09-13;2018-09-14;2018-09-17;2018-09-18;2018-09-19;2018-09-20;2018-09-21;2018-09-25;2018-09-26;2018-09-27;2018-09-28;2018-10-08;2018-10-09;2018-10-10;2018-10-11;2018-10-12;2018-10-15;2018-10-16;2018-10-17;2018-10-18;2018-10-19;2018-10-22;2018-10-23;2018-10-24;2018-10-25;2018-10-26;2018-10-29;2018-10-30;2018-10-31;2018-11-01;2018-11-02;2018-11-05;2018-11-06;2018-11-07;2018-11-08;2018-11-09;2018-11-12;2018-11-13;2018-11-14;2018-11-15;2018-11-16;2018-11-19;2018-11-20;2018-11-21;2018-11-22;2018-11-23;2018-11-26;2018-11-27;2018-11-28;2018-11-29;2018-11-30;2018-12-03;2018-12-04;2018-12-05;2018-12-06;2018-12-07;2018-12-10;2018-12-11;2018-12-12;2018-12-13;2018-12-14;2018-12-17;2018-12-18;2018-12-19;2018-12-20;2018-12-21;2018-12-24;2018-12-25;2018-12-26;2018-12-27;2018-12-28;2018-12-31;"
    if str != "":
        dates = str.split(";")
    else: return None
    return dates

def get_k_data(df, start, end):
    ret = df[(df['date'] >= start) & (df['date'] <= end)]
    return ret

def isOpen(date):
    OpenDates = getOpenDates()
    str = ";".join(OpenDates)
    return date in str

def preOpenDate(date, leftCount=1):
    OpenDates = getOpenDates()
    index = 0
    for d in OpenDates:
        if d == date:
            return OpenDates[index - int(leftCount)]
        index = index + 1
    return None

def getLastestOpenDate(date=getYMD()):
    hms = getHMS()
    if hms >= '15:00:00' and isOpen(date):
        return date
    if hms < '15:00:00' and isOpen(date):
        return preOpenDate(date, 1)
    count = 0
    while True:
        count = count + 1
        if isOpen(date) == False:
            date = getPreDayYMD(1, date)
            continue
        else:
            break
    return date

def nextOpenDate(date, rightCount=1):
    OpenDates = getOpenDates()
    index = 0
    for d in OpenDates:
        if d == date:
            if index + rightCount < OpenDates.__len__() -1:
                return OpenDates[index + rightCount]
            else:
                break
        index = index + 1
    return None





# def getOpenDates():
#     OpenList = ts.trade_cal()
#     dates = []
#     rows = OpenList[OpenList.isOpen == 1].values[-888:]
#     for row in rows:
#         dates.append(row[0])
#     return dates
# def isOpen(date):
#     #OpenList = ts.trade_cal()
#     # try:
#     #     isOpen = OpenList[OpenList.calendarDate == date].values[0][1]
#     # except:
#     #     return None
#     # if (isOpen == 1):
#     #     return True
#     # return False
#     str = ";".join(OpenDates)
#     return date in str
# def get_today_open2close_chg(code, date=getYMD()):
#     try :
#         start = preOpenDate(date, 1)
#         end = start
#         if isinstance(code, str):
#             d = ts.get_k_data(code=code, start=start, end=end)
#         else:
#             d = get_k_data(df=code, start=start, end=end)
#         dc = d['close']
#         do = d['open']
#         ye_open = do.values[0]
#         ye_close = dc.values[0]
#         ret = round(((float(ye_close) - float(ye_open)) / float(ye_open)), 4) * 100
#     except Exception as e:
#         print(e)
#         return None
#     return ret
#
# def get_ye_chg(code, date=getYMD()):
#     try:
#         start = preOpenDate(date, 2)
#         end = preOpenDate(date, 1)
#         if isinstance(code, str):
#             d = ts.get_k_data(code=code, start=start, end=end)
#         else:
#             d = get_k_data(df=code, start=start, end=end)
#         dd = d['close']
#         ty_close = dd.values[0]
#         ye_close = dd.values[1]
#         ret = round(((float(ye_close) - float(ty_close)) / float(ty_close)), 4) * 100
#     except Exception as e:
#         print(e)
#         return None
#     return ret
#
# def get_ty_chg(code, date=getYMD()):
#     try:
#         start = preOpenDate(date, 3)
#         end = preOpenDate(date, 2)
#         if isinstance(code, str):
#             d = ts.get_k_data(code=code, start=start, end=end)
#         else:
#             d = get_k_data(df=code, start=start, end=end)
#         dd = d['close']
#         ty_close = dd.values[0]
#         ye_close = dd.values[1]
#         ret = round(((float(ye_close) - float(ty_close)) / float(ty_close)), 4) * 100
#     except Exception as e:
#         print(e)
#         return None
#     return ret
#
# def get_continuous_rise_day_count(code, date=getYMD()):
#     count = 0
#     try:
#         #chg = get_ye_chg(code, preOpenDate(date, count))
#         chg = get_today_open2close_chg(code, preOpenDate(date, count))
#         while chg >= 0:
#             if count > 10:
#                 break
#             count = count + 1
#             #chg = get_ye_chg(code, preOpenDate(date, count))
#             chg = get_today_open2close_chg(code, preOpenDate(date, count))
#             if chg is None:
#                 break
#     except Exception as e:
#         print(e)
#         return None
#     return count
#
# def get_continuous_z_day_count(code, date=getYMD()):
#     count = 0
#     try:
#         chg = get_ye_chg(code, preOpenDate(date, count))
#         #chg = get_today_open2close_chg(code, preOpenDate(date, count))
#         while chg >= 0:
#             if count > 10:
#                 break
#             count = count + 1
#             chg = get_ye_chg(code, preOpenDate(date, count))
#             #chg = get_today_open2close_chg(code, preOpenDate(date, count))
#             if chg is None:
#                 break
#     except Exception as e:
#         print(e)
#         return None
#     return count
#
# def get_ye_qrr(code, date=getYMD()):
#     try:
#         start = preOpenDate(date, 6)
#         end = preOpenDate(date, 1)
#         if isinstance(code, str):
#             d = ts.get_k_data(code=code, start=start, end=end)
#         else:
#             d = get_k_data(df=code, start=start, end=end)
#         dd = d['volume']
#         len = dd.values.__len__()
#         total_volume = 0
#         ye_volume = 0
#         count = 0
#         for row in dd.values:
#             if count == len - 1:
#                 ye_volume = row
#             else:
#                 total_volume = total_volume + row
#             count = count + 1
#         base = total_volume / (4*60*5)
#         today = ye_volume / (4*60)
#         if base == 0:
#             return None
#         ret = round(float(today/base), 2)
#     except Exception as e:
#         print(e)
#         return None
#     return ret
#
# # def get_ye_tr(code, date=getYMD()):
# #     start = preOpenDate(date, 1)
# #     end = preOpenDate(date, 1)
# #     if isinstance(code, str):
# #         d = ts.get_k_data(code=code, start=start, end=end)
# #     else:
# #         d = get_k_data(df=code, start=start, end=end)
# #         code = d['code'].values[0]
# #         d = ts.get_hist_data(code, start, end)
# #     dd = d['turnover']
# #     print()
#
# def get_open_chg(code, date=getYMD()):
#     try:
#         start = preOpenDate(date, 1)
#         end = date
#         if isinstance(code, str):
#             d = ts.get_k_data(code=code, start=start, end=end)
#         else:
#             d = get_k_data(df=code, start=start, end=end)
#         pre_close = d['close'].values[0]
#         open = d['open'].values[1]
#         ret = round(((float(open) - float(pre_close)) / float(pre_close)), 4) * 100
#     except Exception as e:
#         print(e)
#     return ret
#
# def get_close_chg(code, date=getYMD()):
#     try:
#         start = preOpenDate(date, 1)
#         end = date
#         if isinstance(code, str):
#             d = ts.get_k_data(code=code, start=start, end=end)
#         else:
#             d = get_k_data(df=code, start=start, end=end)
#         pre_close = d['close'].values[0]
#         close = d['close'].values[1]
#         ret = round(((float(close) - float(pre_close)) / float(pre_close)), 4) * 100
#     except Exception as e:
#         print(e)
#     return ret

# dataf = ts.get_k_data('000565', start="2018-07-06", end="2018-07-20")
# print("open_chg: " + str(get_open_chg(dataf, "2018-07-20")))
# print("close_chg: " + str(get_close_chg(dataf, "2018-07-20")))

#initOpenDateTempFile()
# print(isOpen("2018-07-21"))
# print(os.path.dirname(__file__))