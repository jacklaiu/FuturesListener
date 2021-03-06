# -*- coding: gbk -*-
import  execjs
import requests
import PyBase.Util as util
import PyBase.Dao as dao
import PyBase.Log as log
import time

SmtpClient_Host = '95.163.200.245'
SmtpClient_Port = 64210

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

def getRateBetweenMaxAndMin_Speed(items):

    min_createtime_o = {'min': 0, 'createtime': '1970-01-01 00:00:00'}
    for item in items:
        price = float(item['f_price'])
        createtime = item['f_createtime']
        if min_createtime_o['min'] == 0 or price <= min_createtime_o['min']:
            min_createtime_o['min'] = price
            min_createtime_o['createtime'] = createtime

    max_createtime_o = {'max': 0, 'createtime': '1970-01-01 00:00:00'}
    for item in items:
        price = float(item['f_price'])
        createtime = item['f_createtime']
        if price >= max_createtime_o['max']:
            max_createtime_o['max'] = price
            max_createtime_o['createtime'] = createtime

    min_createtime = min_createtime_o['createtime']
    max_createtime = max_createtime_o['createtime']
    min_price = min_createtime_o['min']
    max_price = max_createtime_o['max']

    if min_createtime > max_createtime:
        if max_price == 0:
            return 0
        return round((min_price - max_price) / max_price * 100, 2)
    else:
        if min_price == 0:
            return 0
        return round((max_price - min_price) / min_price * 100, 2)

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

        pre_close = float(lastest['f_pre_close'])
        price = float(lastest['f_price'])
        rate = round((price - pre_close) / pre_close * 100, 2)
        speed = getRateBetweenMaxAndMin_Speed(items)

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
            url = 'http://'+SmtpClient_Host+':'+str(SmtpClient_Port)+'/smtpclient/sendFuture/(Rate: ' + str(rate) + ' Speed: ' + str(
                speed) + ')This is ' + code + '/This is ' + code + '/jacklaiu@163.com'
            #util.Async_req(url).start()
            dao.update(
                "insert into t_future_unusual_action(f_code, f_name, f_speed, f_rate, f_createtime)"
                " values(%s,%s,%s,%s,%s)",
                (code, code_name_rel[code], speed, rate, util.getYMDHMS()))
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
        pre_close = float(lastest['f_pre_close'])
        price = float(lastest['f_price'])
        rate = round((price - pre_close) / pre_close * 100, 2)
        speed = getRateBetweenMaxAndMin_Speed(items)

        if speed < -0.7:
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
            url = 'http://'+SmtpClient_Host+':'+str(SmtpClient_Port)+'/smtpclient/sendFuture/(Rate: ' + str(rate) + ' Speed: ' + str(
                speed) + ')This is ' + code + '/This is ' + code + '/jacklaiu@163.com'

            #util.Async_req(url).start()
            dao.update(
                "insert into t_future_unusual_action(f_code, f_name, f_speed, f_rate, f_createtime)"
                " values(%s,%s,%s,%s,%s)",
                (code, code_name_rel[code], speed, rate, util.getYMDHMS()))
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
        pre_close = float(lastest['f_pre_close'])
        price = float(lastest['f_price'])
        rate = round((price - pre_close) / pre_close * 100, 2)
        speed = getRateBetweenMaxAndMin_Speed(items)

        if speed < -1.0:
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
            url = 'http://'+SmtpClient_Host+':'+str(SmtpClient_Port)+'/smtpclient/sendFuture/(Rate: ' + str(rate) + ' Speed: ' + str(
                speed) + ')This is ' + code + '/This is ' + code + '/jacklaiu@163.com'
            #util.Async_req(url).start()
            dao.update(
                "insert into t_future_unusual_action(f_code, f_name, f_speed, f_rate, f_createtime)"
                " values(%s,%s,%s,%s,%s)",
                (code, code_name_rel[code], speed, rate, util.getYMDHMS()))
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
            if line == '': continue
            try:
                code = line[line.index("str_") + 4: line.index('=') - 1].upper()
            except:
                continue
            if util.isOpenTime_Kind(code) is False:
                continue
            if '"' not in line: continue
            line = line[line.index('"') + 1: line.rindex('"')]
            if line.__len__() == 0: continue
            cols = line.split(",")
            name = cols[0]
            pre_close = float(cols[5])
            price = float(cols[8])
            position = float(cols[13])
            settlement_price = float(cols[9])
            date = cols[17]
            log.log("名称：" + name + " 昨收：" + str(pre_close) + " 现价：" + str(price) + " 收盘价：" + str(round((price - pre_close)/pre_close * 100, 2)))
            values.append((code, name, date, price, pre_close, position, settlement_price, util.getHMS(), util.getYMDHMS()))
            count = count + 1
        dao.updatemany("insert into"
                       " t_future_tick(f_code, f_name, f_date, f_price, f_pre_close,"
                       " f_position, f_settlement_price, f_time, f_createtime)"
                       " values(%s,%s,%s,%s,%s,%s,%s,%s,%s)", values)

        notify5min()
        notify10min()
        notify15min()
        print("loop next need sleep")
        time.sleep(25)

print("Start Listen Futures")
listen()
# print(util.timeDur_ReturnSec('2018-08-27 00:00:00', util.getYMDHMS()))




