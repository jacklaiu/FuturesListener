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
    # �Ϻ��ڻ�������
    #'AG': '����',
    #'CU': '��ͭ',
    #'AL': '����',
    #'ZN': '��п',
    'RU': '��',
    #'FU': 'ȼ��',
    #'PB': '��Ǧ',
    'RB': '����',
    #'WR': '�߲�',
    #'AU': '����',
    'BU': '����',
    'HC': '�Ⱦ�',
    #'NI': '����',
    #'SN': '����',
    # ������Ʒ������
    'A': '��һ',
    'B': '����',
    'M': '����',
    'J': '��̿',
    'JM': '��ú',
    'C': '����',
    'Y': '����',
    'L': '����',
    'PP': 'PP',
    'V': 'PVC',
    'P': '���',
    'JD': '����',
    'I': '����',
    'FB': '�˰�',
    #'BB': '����',
    'CS': '���',
    # ֣����Ʒ������
    'AP': 'ƻ��',
    #'WH': 'ǿ��',
    #'PM': '����',
    'FG': '����',
    'MA': '�״�',
    'SF': '����',
    'SM': '����',
    #'RI': '�絾',
    'CF': '�޻�',
    'SR': '����',
    'OI': '����',
    #'RS': '����',
    'RM': '����',
    'TA': 'RTA',
    'ZC': '��ú'
    #'JR': '����',
    #'LR': '��',
    #'CY': '��ɴ'
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
            # �ٴη���֪ͨ��CDʱ��
            if code in coolDown_5min.keys():
                now = util.getYMDHMS()
                coolDown_5min_starttime = coolDown_5min[code]
                durSec = util.timeDur_ReturnSec(coolDown_5min_starttime, now)
                if durSec < 60 * 30:
                    return
                else:
                    coolDown_5min.pop(code)
            # ����֪ͨ
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
            # �ٴη���֪ͨ��CDʱ��
            if code in coolDown_10min.keys():
                now = util.getYMDHMS()
                coolDown_10min_starttime = coolDown_10min[code]
                durSec = util.timeDur_ReturnSec(coolDown_10min_starttime, now)
                if durSec < 60 * 30:
                    return
                else:
                    coolDown_10min.pop(code)
            # ����֪ͨ
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
            # �ٴη���֪ͨ��CDʱ��
            if code in coolDown_15min.keys():
                now = util.getYMDHMS()
                coolDown_15min_starttime = coolDown_15min[code]
                durSec = util.timeDur_ReturnSec(coolDown_15min_starttime, now)
                if durSec < 60 * 30:
                    return
                else:
                    coolDown_15min.pop(code)
            # ����֪ͨ
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
            #print("���ƣ�" + name + " ���գ�" + str(pre_close) + " �ּۣ�" + str(price) + " ���̼ۣ�" + str(round((price - pre_close)/pre_close * 100, 2)))
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




