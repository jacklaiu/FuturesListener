# -*- coding: gbk -*-
import  execjs
import requests
import PyBase.Util as util
import PyBase.Dao as dao
import PyBase.Log as log
import time

exchange_code_rel = {

    'SHFE': ['RU', 'RB', 'BU', 'HC'],

    'CZCE': ['A', 'B', 'M', 'J', 'JM', 'C', 'Y', 'L', 'PP', 'V', 'P', 'JD', 'I', 'FB', 'CS'],

    'DCE':  ['AP','FG','MA','SF','SM','CF','SR','OI','RM','TA','ZC']

}

code_name_rel = {
    # 上海期货交易所
    #'AG': '沪银',
    #'CU': '沪铜',
    #'AL': '沪铝',
    #'ZN': '沪锌',
    'RU': '橡胶',
    #'FU': '燃油',
    #'PB': '沪铅',
    'RB': '螺纹',
    #'WR': '线材',
    #'AU': '沪金',
    'BU': '沥青',
    'HC': '热卷',
    #'NI': '沪镍',
    #'SN': '沪锡',
    # 大连商品交易所
    'A': '豆一',
    'B': '豆二',
    'M': '豆粕',
    'J': '焦炭',
    'JM': '焦煤',
    'C': '玉米',
    'Y': '豆油',
    'L': '塑料',
    'PP': 'PP',
    'V': 'PVC',
    'P': '棕榈',
    'JD': '鸡蛋',
    'I': '铁矿',
    'FB': '纤板',
    #'BB': '胶板',
    'CS': '淀粉',
    # 郑州商品交易所
    'AP': '苹果',
    #'WH': '强麦',
    #'PM': '普麦',
    'FG': '玻璃',
    'MA': '甲醇',
    'SF': '硅铁',
    'SM': '硅锰',
    #'RI': '早稻',
    'CF': '棉花',
    'SR': '白糖',
    'OI': '菜油',
    #'RS': '菜籽',
    'RM': '菜粕',
    'TA': 'RTA',
    'ZC': '动煤'
    #'JR': '粳稻',
    #'LR': '晚稻',
    #'CY': '棉纱'
}

coolDown_5min = {}
coolDown_10min = {}
coolDown_15min = {}

def getUrl(symbols):
    count = 0
    url = "http://hq.sinajs.cn/list="
    for code in symbols:
        if count == symbols.__len__() - 1:
            url = url + code + "0"
        else:
            url = url + code + '0,'
        count = count + 1
    return url

def notify5min():
    # --------------------------------------------------------------------------------------------------------------------------------------------
    items = dao.select("select f_code, f_name, f_price, f_pre_close, f_createtime from t_future_tick where"
                       " f_createtime > date_add(now(), interval - 5 minute) order by f_createtime desc", ())
    code_items_rel = {}
    for item in items:
        code = item['f_code']
        if code not in code_items_rel.keys():
            code_items_rel.setdefault(code, [item])
        else:
            code_items_rel[code].append(item)

    for code in code_items_rel.keys():
        items = code_items_rel[code]
        if items.__len__() < 2:
            continue
        lastest = items[0]
        _5minago_item = items[-1]
        pre_close = float(lastest['f_pre_close'])
        _5minago_price = float(_5minago_item['f_price'])
        if _5minago_price == 0 or pre_close == 0:
            continue
        latest_Price = float(lastest['f_price'])
        rate = round((latest_Price - pre_close) / pre_close * 100, 2)
        speed = round((latest_Price - _5minago_price) / _5minago_price * 100, 2)

        if speed > 0.5 or speed < -0.5:
            # 再次发送通知的CD时间
            if code in coolDown_5min.keys():
                now = util.getYMDHMS()
                coolDown_5min_starttime = coolDown_5min[code]
                durSec = util.timeDur_ReturnSec(coolDown_5min_starttime, now)
                if durSec < 60 * 30:
                    return
                else:
                    coolDown_5min.pop(code)
            # 发送通知
            log.log("Send Notification: " + code + " speed: " + str(speed))
            url = 'http://95.163.200.245:64210/smtpclient/sendPlain/(Rate: ' + str(rate) + ' Speed: ' + str(
                speed) + ')This is ' + code + '/This is ' + code + '/jacklaiu@qq.com'
            util.Async_req(url).start()
            coolDown_5min.setdefault(code, util.getYMDHMS())

def notify10min():
    # --------------------------------------------------------------------------------------------------------------------------------------------
    items = dao.select("select f_code, f_name, f_price, f_pre_close, f_createtime from t_future_tick where"
                       " f_createtime > date_add(now(), interval - 10 minute) order by f_createtime desc", ())
    code_items_rel = {}
    for item in items:
        code = item['f_code']
        if code not in code_items_rel.keys():
            code_items_rel.setdefault(code, [item])
        else:
            code_items_rel[code].append(item)

    for code in code_items_rel.keys():
        items = code_items_rel[code]
        if items.__len__() < 2:
            continue
        lastest = items[0]
        _5minago_item = items[-1]
        pre_close = float(lastest['f_pre_close'])
        _5minago_price = float(_5minago_item['f_price'])
        if _5minago_price == 0 or pre_close == 0:
            continue
        latest_Price = float(lastest['f_price'])
        rate = round((latest_Price - pre_close) / pre_close * 100, 2)
        speed = round((latest_Price - _5minago_price) / _5minago_price * 100, 2)

        if speed > 0.7 or speed < -0.7:
            # 再次发送通知的CD时间
            if code in coolDown_10min.keys():
                now = util.getYMDHMS()
                coolDown_10min_starttime = coolDown_10min[code]
                durSec = util.timeDur_ReturnSec(coolDown_10min_starttime, now)
                if durSec < 60 * 30:
                    return
                else:
                    coolDown_10min.pop(code)
            # 发送通知
            log.log("Send Notification: " + code + " speed: " + str(speed))
            url = 'http://95.163.200.245:64210/smtpclient/sendPlain/(Rate: ' + str(rate) + ' Speed: ' + str(
                speed) + ')This is ' + code + '/This is ' + code + '/jacklaiu@qq.com'
            util.Async_req(url).start()
            coolDown_10min.setdefault(code, util.getYMDHMS())

def notify15min():
    # --------------------------------------------------------------------------------------------------------------------------------------------
    items = dao.select("select f_code, f_name, f_price, f_pre_close, f_createtime from t_future_tick where"
                       " f_createtime > date_add(now(), interval - 15 minute) order by f_createtime desc", ())
    code_items_rel = {}
    for item in items:
        code = item['f_code']
        if code not in code_items_rel.keys():
            code_items_rel.setdefault(code, [item])
        else:
            code_items_rel[code].append(item)

    for code in code_items_rel.keys():
        items = code_items_rel[code]
        if items.__len__() < 2:
            continue
        lastest = items[0]
        _5minago_item = items[-1]
        pre_close = float(lastest['f_pre_close'])
        _5minago_price = float(_5minago_item['f_price'])
        if _5minago_price == 0 or pre_close == 0:
            continue
        latest_Price = float(lastest['f_price'])
        rate = round((latest_Price - pre_close) / pre_close * 100, 2)
        speed = round((latest_Price - _5minago_price) / _5minago_price * 100, 2)

        if speed > 1.0 or speed < -1.0:
            # 再次发送通知的CD时间
            if code in coolDown_15min.keys():
                now = util.getYMDHMS()
                coolDown_15min_starttime = coolDown_15min[code]
                durSec = util.timeDur_ReturnSec(coolDown_15min_starttime, now)
                if durSec < 60 * 30:
                    return
                else:
                    coolDown_15min.pop(code)
            # 发送通知
            log.log("Send Notification: " + code + " speed: " + str(speed))
            url = 'http://95.163.200.245:64210/smtpclient/sendPlain/(Rate: ' + str(rate) + ' Speed: ' + str(
                speed) + ')This is ' + code + '/This is ' + code + '/jacklaiu@qq.com'
            util.Async_req(url).start()
            coolDown_15min.setdefault(code, util.getYMDHMS())

def listen():
    while True:
        if util.isOpenTime_wide() is False:
            time.sleep(10)
            continue
        url = getUrl(code_name_rel.keys())
        ctn = requests.get(url).text
        strs = ctn.split("\n")
        values = []
        count = 0
        for line in strs:
            code = line[line.index("str_") + 4: line.index('=') - 1].upper()
            if util.isOpenTime_Kind(code) is False:
                continue
            if '"' not in line: continue
            line = line[line.index('"') + 1: line.rindex('"')]
            if line.__len__() == 0: continue
            cols = line.split(",")
            name = cols[0]
            pre_close = float(cols[5])
            price = float(cols[8])
            date = cols[17]
            #print("名称：" + name + " 昨收：" + str(pre_close) + " 现价：" + str(price) + " 收盘价：" + str(round((price - pre_close)/pre_close * 100, 2)))
            values.append((code, name, date, price, pre_close, util.getHMS(), util.getYMDHMS()))
            count = count + 1
        dao.updatemany("insert into t_future_tick(f_code, f_name, f_date, f_price, f_pre_close, f_time, f_createtime)"
                       " values(%s,%s,%s,%s,%s,%s,%s)", values)

        notify5min()
        notify10min()
        notify15min()
        time.sleep(30)

print("Start Listen Futures")
listen()
# print(util.timeDur_ReturnSec('2018-08-27 00:00:00', util.getYMDHMS()))




