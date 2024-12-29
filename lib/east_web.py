#!/usr/bin/env python
# -*- coding=UTF-8 -*-
import urllib.request
import json
import decimal
import time
import random
import sys
import hashlib
import lib.public as public
import requests
from DrissionPage import ChromiumPage, ChromiumOptions


class east_web(object):

    _t = '0014416471786912188'
    delay_min = 1
    delay_max = 3

    def __init__(self):
        # self._t = round(time.time()*1000)
        self.pageNo = public.get('page')
        self.pageSize = public.get('limit')
        pass

    def delay_sleep(self):
        delay = random.uniform(self.delay_min, self.delay_max)
        print("delay:" + str(delay))
        time.sleep(delay)

    def help(self):
        return (list(filter(lambda m:
                            not m.startswith("__") and
                            not m.endswith("__") and
                            not m.startswith("_") and
                            not m.startswith("dump") and
                            not m.startswith("methods") and
                            callable(getattr(self, m)), dir(self))))

    # 获取基金信息
    def get_fund(self, secid, fields='f43'):
        return self.get_info(secid, fields)

    def get_fund_top(self):
        fields = 'SECURITY_NAME_ABBR,SECURITY_CODE,CHANGE_RATE,NEW_PRICE'
        self.get_fund_list(p=self.pageNo,ps=self.pageSize,sort_str = '-1,-1,1',fields = fields,is_print=True)

    def get_fund_low(self):
        fields = 'SECURITY_NAME_ABBR,SECURITY_CODE,CHANGE_RATE,NEW_PRICE'
        self.get_fund_list(p=self.pageNo,ps=self.pageSize,sort_str = '1,1,1',fields = fields,is_print=True)

    def get_fund_top_t0(self):
        fields = 'SECURITY_NAME_ABBR,SECURITY_CODE,CHANGE_RATE,NEW_PRICE'
        self.get_fund_list(p=self.pageNo, ps=self.pageSize,filter='(ETF_TYPE_CODE%3D%22ALL%22)(IS_TPLUS%3D%221%22)', sort_str='-1,-1,1', fields=fields, is_print=True)

    def get_fund_low_t0(self):
        fields = 'SECURITY_NAME_ABBR,SECURITY_CODE,CHANGE_RATE,NEW_PRICE'
        self.get_fund_list(p=self.pageNo, ps=self.pageSize,filter='(ETF_TYPE_CODE%3D%22ALL%22)(IS_TPLUS%3D%221%22)', sort_str='1,1,1', fields=fields, is_print=True)

    # 获取基金列表
    def get_fund_list(self, p = 1, ps = 1, filter='(ETF_TYPE_CODE%3D%22ALL%22)',sort_str = '-1,-1,1', fields='SECURITY_NAME_ABBR,SECURITY_CODE,CHANGE_RATE,NEW_PRICE,SECUCODE,IS_TPLUS',is_print = False):
        url = 'https://datacenter.eastmoney.com/stock/fundselector/api/data/get?type=RPTA_APP_FUNDSELECT&sty=IS_TPLUS,SECUCODE,SECURITY_CODE,CHANGE_RATE_1W,CHANGE_RATE_1M,CHANGE_RATE_3M,YTD_CHANGE_RATE,DEC_TOTALSHARE,DEC_NAV,SECURITY_NAME_ABBR,DERIVE_INDEX_CODE,INDEX_CODE,INDEX_NAME,NEW_PRICE,CHANGE_RATE,CHANGE,VOLUME,DEAL_AMOUNT,PREMIUM_DISCOUNT_RATIO,QUANTITY_RELATIVE_RATIO,HIGH_PRICE,LOW_PRICE,STOCK_ID&extraCols=&source=FUND_SELECTOR&client=APP&filter={}&p={}&ps={}&st=CHANGE_RATE,CHANGE,SECURITY_CODE&sr={}'.\
            format(filter,p,ps,sort_str)

        data = self.__curl(url)
        data_list = data['result']['data']
        result = []
        for row in data_list:
            if type(row) == str:
                row = data_list[row]
            secucode= row['SECUCODE'].split('.')[1]
            if secucode == 'SH':
                row['SECUCODE'] = 1
            elif secucode == 'SZ':
                row['SECUCODE'] = 0
            else:
                print(row['SECUCODE'])
                sys.exit('error market')

            if fields == '':
                item = row
            else:
                item = self._field(fields, row)

            result.append(item)

        if is_print:
            self.dump(result)
        else:
            return result

    # 获取股票信息
    def get_info(self, secid, fields='f43'):
        url = 'https://push2.eastmoney.com/api/qt/stock/get?secid={}&ut=f057cbcbce2a86e2866ab8877db1d059&forcect=1&fields=f13,f19,f20,f23,f24,f25,f26,f27,f28,f29,f30,f43,f44,f45,f46,f47,f48,f49,f50,f57,f58,f59,f60,f85,f107,f111,f113,f114,f115,f116,f117,f127,f130,f131,f132,f133,f135,f136,f137,f138,f139,f140,f141,f142,f143,f144,f145,f146,f147,f148,f149,f152,f161,f162,f164,f165,f167,f168,f169,f170,f171,f174,f175,f177,f178,f181,f182,f198,f199,f260,f261,f288,f292,f293,f294,f295,f530,f531,f51,f52&invt=2&_={}' \
            .format(secid, self._t)
        result = self.__curl(url)
        data = result['data']
        return self._field(fields, data)

    # 获取股票日金额
    def get_day_info(self,secid):
        url = ('https://push2his.eastmoney.com/api/qt/stock/kline/get?secid={}&klt=101&fqt=1&lmt=66&end=20500000&iscca=1&fields1=f1,f2,f3,f4,f5,f6,f7,f8&fields2=f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61,f62,f63,f64&ut=f057cbcbce2a86e2866ab8877db1d059&forcect=1'\
               .format(secid))
        result = self.__curl(url)
        data = result['data']['klines']
        data_days = []
        for item in list(reversed(data)):
            item_val = item.split(',')
            data_days.append(item_val)
        return data_days

    def get_days_info(self,secid,data = None):
        if data == None:
            data = self.get_day_info(secid)
        num5 = 5
        num10 = 10
        num20 = 20

        price5 = round(sum([float(i[2]) for i in data[0:num5]]) / num5,2)
        price10 = round(sum([float(i[2]) for i in data[0:num10]]) / num10, 2)
        price20 = round(sum([float(i[2]) for i in data[0:num20]]) / num20, 2)

        rate5 = round(sum([float(i[8]) for i in data[0:num5]]) / num5, 2)
        rate10 = round(sum([float(i[8]) for i in data[0:num10]]) / num10, 2)
        rate20 = round(sum([float(i[8]) for i in data[0:num20]]) / num20, 2)

        days_rate = [float(i[8]) for i in data[0:num20]]
        rate_max = max(days_rate)
        rate_min = min(days_rate)

        price = float(data[0][2])
        rate = float(data[0][8])

        price_avg = round(sum(list([price5,price10,price20])) / 3,2)
        price_diff = round(price - price_avg,2)

        rate_avg = round(sum(list([rate5, rate10, rate20])) / 3, 2)
        rate_diff = round(sum(list([abs(rate_max), abs(rate_min)])) / 2, 2)
        rate_yq = round(rate_diff/2, 2)

        rate_diff_avg = round((price - price_avg)/price * 100, 4)

        is_yq = 0
        if abs(rate_avg) <=  0.2 and rate_diff > 3 and rate_diff < 8:
            if rate > 0 and rate >= rate_yq:
                # 卖出信号
                is_yq = 2
            elif rate < 0 and rate <= rate_avg * -1:
                #买入信号
                is_yq = 1
            else:
                # 持有
                is_yq = 3
        elif rate > 5:
            # 突破
            is_yq = 10
        elif rate < -5:
            # 加速下跌
            is_yq = 11
        else:
            #未建模
            is_yq = 12

        result = {
            'price5':price5,
            'price10': price10,
            'price20': price20,
            'price_avg': price_avg,
            'price_diff': price_diff,
            'rate': rate,
            'rate_max': rate_max,
            'rate_min': rate_min,
            'rate_avg': rate_avg,
            'rate_diff': rate_diff,
            'rate_diff_avg': rate_diff_avg,
            'rate_yq': rate_yq,
            'is_yq': is_yq
        }
        return result


    # 获取股票的板块信息
    def get_stock_bk(self, code, fields):
        url = 'https://push2.eastmoney.com/api/qt/slist/get?ut=f057cbcbce2a86e2866ab8877db1d059&forcect=1&spt=3&fields=f1,f12,f152,f3,f14,f128,f136&pi=0&pn={}&pz={}&po=1&fid=f3&invt=2&secid={}&_={}' \
            .format(self.pageNo,self.pageSize,code, self._t)
        result = self.__curl(url)
        list = result['data']['diff']
        data = []
        for index in list:
            row = list[index]
            item = self._field(fields, row)
            data.append(item)
        return data

    def get_bk_stock(self, code, fields):
        url = 'https://push2.eastmoney.com/api/qt/clist/get?ut=f057cbcbce2a86e2866ab8877db1d059&forcect=1&fs={}&pn={}&pz={}&po=1&fid=f3&invt=2&_={}' \
            .format(code,self.pageNo,self.pageSize, self._t)
        result = self.__curl(url)
        list = result['data']['diff']
        data = []
        for index in list:
            row = list[index]
            item = self._field(fields, row)
            data.append(item)
        return data

    def get_index(self):
        url = 'https://push2.eastmoney.com/api/qt/ulist.np/get?fltt=2&invt=2&fields=f1,f2,f3,f4,f6,f12,f13,f14,f62&secids=1.000001,0.399001,0.399006,1.000688,100.HSI,1.000300,0.399005&ut=f057cbcbce2a86e2866ab8877db1d059&forcect=1&_={}' \
            .format(self._t)
        self._get('指数', url, 'f14,f2,f3:0:%,f6:8:亿,f62:0:')

    def get_bk(self, page=1, limit=10, fields='f14,f12,f3,f128,f140,f136', is_print=True):
        url = 'https://push2.eastmoney.com/api/qt/clist/get?pn={}&pz={}&po=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f3&fs=m:90&fields=f3,f4,f12,f13,f14,f128,f136,f127&_={}' \
            .format(str(page), str(limit), self._t)
        # print(url)
        if is_print:
            self._get('板块', url, fields, is_print)
        else:
            return self._get('板块', url, fields, is_print)

    def get_bk_industry(self):
        url = 'https://push2.eastmoney.com/api/qt/clist/get?pn={}&pz={}&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f3&fs=m:90+t:2+f:!50&fields=f3,f4,f12,f13,f14,f128,f136&_={}' \
            .format(self.pageNo,self.pageSize,self._t)
        self._get('板块行业', url, 'f14,f12,f3,f128,f140,f136')

    def get_bk_concept(self):
        url = 'https://push2.eastmoney.com/api/qt/clist/get?pn={}&pz={}&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f3&fs=m:90+t:3+f:!50&fields=f3,f4,f12,f13,f14,f128,f136&_={}' \
            .format(self.pageNo,self.pageSize,self._t)
        self._get('板块概念', url, 'f14,f12,f3,f128,f140,f136')

    def get_bk_area(self):
        url = 'https://push2.eastmoney.com/api/qt/clist/get?pn={}&pz={}&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f3&fs=m:90+t:1+f:!50&fields=f3,f4,f12,f13,f14,f128,f136&_={}' \
            .format(self.pageNo,self.pageSize,self._t)
        self._get('板块地区', url, 'f14,f12,f3,f128,f140,f136')

    def get_stock_top(self):
        url = 'https://push2.eastmoney.com/api/qt/clist/get?ut=7eea3edcaed734bea9cbfc24409ed989&pn={}&pz={}&po=1&np=1&fltt=2&invt=2&fid=f3&fs=m:0+t:6+f:!2,m:0+t:13+f:!2,m:0+t:80+f:!2,m:1+t:2+f:!2,m:1+t:23+f:!2&fields=f2,f3,f4,f12,f13,f14,f19,f148?cb=?&_={}' \
            .format(self.pageNo,self.pageSize, self._t)
        self._get('涨幅榜', url, 'f14,f12,f2,f3:-1:%')

    def get_stock_low(self):
        url = 'https://push2.eastmoney.com/api/qt/clist/get?pn={}&pz={}&po=0&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f3&fs=m:0+t:6+f:!2,m:0+t:13+f:!2,m:0+t:80+f:!2,m:1+t:2+f:!2,m:1+t:23+f:!2&fields=f2,f3,f4,f12,f13,f14,f19,f148?cb=?&_={}' \
            .format(self.pageNo,self.pageSize,self._t)
        self._get('跌幅榜', url, 'f14,f12,f3,f2')

    def get_stock_input(self):
        url = 'https://push2.eastmoney.com/api/qt/clist/get?pn={}&pz={}&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f62&fs=m:0+t:6+f:!2,m:0+t:13+f:!2,m:0+t:80+f:!2,m:1+t:2+f:!2,m:1+t:23+f:!2&fields=f2,f3,f4,f12,f13,f14,f19,f62,f148?cb=?&_={}' \
            .format(self.pageNo,self.pageSize,self._t)
        self._get('净流入', url, 'f14,f12,f3,f2,f62')

    def get_stock_change(self):
        url = 'https://push2.eastmoney.com/api/qt/clist/get?pn={}&pz={}&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f8&fs=m:0+t:6+f:!2,m:0+t:13+f:!2,m:0+t:80+f:!2,m:1+t:2+f:!2,m:1+t:23+f:!2&fields=f2,f3,f4,f8,f12,f13,f14,f19,f148?cb=?&_={}' \
            .format(self.pageNo,self.pageSize,self._t)
        self._get('换手率', url, 'f14,f12,f3,f2,f8')

    def get_stock_amount(self):
        url = 'https://push2.eastmoney.com/api/qt/clist/get?pn={}&pz={}&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f10&fs=m:0+t:6+f:!2,m:0+t:13+f:!2,m:0+t:80+f:!2,m:1+t:2+f:!2,m:1+t:23+f:!2&fields=f2,f3,f4,f8,f10,f12,f13,f14,f19,f148&_={}' \
            .format(self.pageNo,self.pageSize,self._t)
        self._get('量比', url, 'f14,f12,f3,f2,f10')

    def get_stock_money(self):
        url = 'https://push2.eastmoney.com/api/qt/clist/get?pn={}&pz={}&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f6&fs=m:0+t:6+f:!2,m:0+t:13+f:!2,m:0+t:80+f:!2,m:1+t:2+f:!2,m:1+t:23+f:!2&fields=f2,f3,f4,f6,f8,f10,f12,f13,f14,f19,f148?cb=?&_={}' \
            .format(self.pageNo,self.pageSize,self._t)
        self._get('成交额', url, 'f14,f12,f3,f2,f6')

    def get_tmp_top(self):
        url = 'https://push2.eastmoney.com/api/qt/clist/get?pn={}&pz={}&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f22&fs=m:0+t:6+f:!2,m:0+t:13+f:!2,m:0+t:80+f:!2,m:1+t:2+f:!2,m:1+t:23+f:!2&fields=f2,f3,f4,f12,f13,f14,f19,f22,f148?cb=?&_={}' \
            .format(self.pageNo,self.pageSize,self._t)
        self._get('涨速榜', url, 'f14,f12,f3,f2,f22')

    def get_tmp_low(self):
        url = 'https://push2.eastmoney.com/api/qt/clist/get?pn={}&pz={}&po=0&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f22&fs=m:0+t:6+f:!2,m:0+t:13+f:!2,m:0+t:80+f:!2,m:1+t:2+f:!2,m:1+t:23+f:!2&fields=f2,f3,f4,f12,f13,f14,f19,f22,f148?cb=?&_={}' \
            .format(self.pageNo,self.pageSize,self._t)
        self._get('跌速榜', url, 'f14,f12,f3,f2,f22')

    def get_tmp_change(self):
        tags = '盘口异动'
        print('{}----------'.format(tags))
        url = 'https://push2.eastmoney.com/api/qt/pkyd/get?ut=bd1d9ddb04089700cf9c27f6f7426281&lmt=9&fields=f1,f2,f3,f4,f5,f6,f7?cb=?&_={}' \
            .format(self._t)
        data = self.__curl(url)
        list = data['data']['pkyd']
        for row_str in list:
            row = row_str.split(',')
            tags = '-'
            if row[6] == '1':
                tags = '+'
            tmp = '{}|{}|{}|{}{}'.format(row[0], row[3], row[1], tags, row[5])
            print(tmp)

    def get_tmp_bk(self):
        url = 'https://push2.eastmoney.com/api/qt/clist/get?pn={}&pz={}&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f22&fs=m:90&fields=f2,f3,f4,f6,f8,f10,f12,f13,f14,f19,f22,f128,f136,f148?cb=?&_={}' \
            .format(self.pageNo,self.pageSize,self._t)
        self._get('板块涨速', url, 'f14,f12,f3,f22,f128,f140,f136')

    def get_kzc(self):
        sortField = 'BondRisePercent'
        url = 'https://emdcmiddleware.eastmoney.com/api/StockPool/BondList?pageSize={}&sortField={}&sortType=0&startIndex=1' \
            .format(self.pageSize, sortField, self._t)
        print('{}----------'.format('可转债'))
        data = self.__curl(url)
        for row in data['Data']['List']:
            str = []
            str.append(row['BondName'])
            str.append(row['BondCode'])
            str.append(row['BondNewPrice'])
            str.append(row['BondRisePercent'])
            str.append(row['SecurityName'])
            str.append(row['SecurityCode'])
            str.append(row['NewPrice'])
            str.append(row['RisePercent'])
            print('|'.join(str))

    def get_kzc_top(self):
        sortField = 'RisePercent'
        url = 'https://emdcmiddleware.eastmoney.com/api/StockPool/BondList?pageSize={}&sortField={}&sortType=0&startIndex=1' \
            .format(self.pageSize, sortField, self._t)
        print('{}----------'.format('可转债'))
        data = self.__curl(url)
        for row in data['Data']['List']:
            str = []
            str.append(row['BondName'])
            str.append(row['BondCode'])
            str.append(row['BondNewPrice'])
            str.append(row['BondRisePercent'])
            str.append(row['SecurityName'])
            str.append(row['SecurityCode'])
            str.append(row['NewPrice'])
            str.append(row['RisePercent'])
            print('|'.join(str))

    def get_market(self):
        print('{}----------'.format('行情'))

        code = '1.000001,0.399001,0.399006,1.000688,100.HSI,1.000300,0.399005'
        url = 'https://push2.eastmoney.com/api/qt/ulist.np/get?fltt=2&invt=2&fields=f1,f2,f3,f4,f6,f12,f13,f14,f62&secids={}&ut=f057cbcbce2a86e2866ab8877db1d059&forcect=1&_={}' \
            .format(code, self._t)

        # print(url)
        index_data = self.__curl(url)

        # print(index_data['data']['diff'][0])
        # sys.exit()
        result_001 = index_data['data']['diff'][0]
        result_002 = index_data['data']['diff'][1]

        index_list = []
        for row in index_data['data']['diff']:
            # str_row = '{}|{}|{}|{}|{}'.format(row['f14'],
            #                                  row['f2'],
            #                                  self._field_type(row['f3'],0,'%'),
            #                                  self._field_type(row['f6'],8,'亿'),
            #                                  self._field_type(row['f62'],8,'亿'))
            index_list.append('{}|{}'.format(str(row['f14'])[0:2], self._field_type(row['f3'], 0, '%')))
        print(' '.join(index_list))

        str003 = '{}|{}|{}'.format('交易',
                                   self._field_type(result_001['f6'] + result_002['f6'], 8, '亿'),
                                   self._field_type(result_001['f62'] + result_002['f62'], 8, '亿'))
        print(str003)
        # ---
        # self.get_money()
        # ---
        url = 'https://datacenter.eastmoney.com/securities/api/data/get?type=RPTAAA_DMSK_TS_CHANGESTATISTICS&?v={}' \
            .format(self._t)
        data = self.__curl(url)
        result = data['result']['data'][0]
        str1 = '++ {}|{}|{} --'.format( result['IND1'], result['INDEX5'],result['IND2'])
        print(str1)
        print('++:{}|+5:{}|+1:{}|+0:{}|{}|-0:{}|-1:{}|-5:{}|{}:--'.format(
            result['IND3'],result['INDEX8'],result['INDEX7'],result['INDEX6'],
             result['INDEX5'],
             result['INDEX4'],result['INDEX3'],result['INDEX2'],result['IND5']))

    def get_money(self):
        url = 'https://datacenter.eastmoney.com/securities/api/data/get?type=RPT_MUTUAL_QUOTA&sty=TRADE_DATE,MUTUAL_TYPE,CLOSED_REASON,BOARD_TYPE,MUTUAL_TYPE_NAME,FUNDS_DIRECTION,INDEX_CODE,INDEX_NAME,START_TIME,END_TIME,BOARD_CODE&callback=&extraCols=status%7C07%7CBOARD_CODE,dayNetAmtIn%7C07%7CBOARD_CODE,dayAmtRemain%7C07%7CBOARD_CODE,dayAmtThreshold%7C07%7CBOARD_CODE,f104%7C07%7CBOARD_CODE,f105%7C07%7CBOARD_CODE,f106%7C07%7CBOARD_CODE,f3%7C03%7CINDEX_CODE%7CINDEX_f3,netBuyAmt%7C07%7CBOARD_CODE&filter=&p=1&ps=200&sr=1&st=MUTUAL_TYPE&token=&var=&source=DataCenter&client=APP'
        data = self.__curl(url)
        result0 = data['result']['data'][0]
        result2 = data['result']['data'][2]

        str1 = '{}|{}'.format(str(result0['BOARD_TYPE'])[0:1], self._field_type(result0['netBuyAmt'], 4, '亿'))
        str2 = '{}|{}'.format(str(result2['BOARD_TYPE'])[0:1], self._field_type(result2['netBuyAmt'], 4, '亿'))
        str3 = '{}|{}'.format('北向', self._field_type(result0['netBuyAmt'] + result2['netBuyAmt'], 4, '亿'))
        print(str3, str1, str2)

    def get_bk_input(self):
        # &filter=(BOARD_TYPE=%221%22)
        sr = '-1'
        url = 'https://datacenter.eastmoney.com/securities/api/data/get?type=RPT_FUNDFLOW_BOARDCODE&sty=ALL&source=SECURITIES&client=WAP&extraCols=f3%7C06%7CINDEX_CODE%7CCHANGE_RATE,MAIN_NETINFLOW%7C06%7CINDEX_CODE%7CMAIN_NETINFLOW&p=1&ps={}&sr={}&st=MAIN_NETINFLOW&?v={}' \
            .format(10, sr, self._t)
        result = self.__curl(url)
        data = result['result']['data']
        data = data[::-1]
        for row in data:
            str = '{}|{}|{}|{}' \
                .format(row['BOARD_NAME'], row['INDEX_CODE'], row['CHANGE_RATE'],
                        self._field_type(row['MAIN_NETINFLOW'], 8, '亿'))
            print(str)

    def get_bk_out(self):
        filter = '&filter=(BOARD_TYPE=%222%22)'
        sr = '1'
        url = 'https://datacenter.eastmoney.com/securities/api/data/get?type=RPT_FUNDFLOW_BOARDCODE&sty=ALL{}&source=SECURITIES&client=WAP&extraCols=f3%7C06%7CINDEX_CODE%7CCHANGE_RATE,MAIN_NETINFLOW%7C06%7CINDEX_CODE%7CMAIN_NETINFLOW&p=1&ps={}&sr={}&st=MAIN_NETINFLOW&?v={}' \
            .format(filter, 10, sr, self._t)
        result = self.__curl(url)
        data = result['result']['data']
        data = data[::-1]
        for row in data:
            str = '{}|{}|{}|{}' \
                .format(row['BOARD_NAME'], row['INDEX_CODE'], row['CHANGE_RATE'],
                        self._field_type(row['MAIN_NETINFLOW'], 8, '亿'))
            print(str)

    def get_hot(self, fields='f14,f12,f2,f3:0:%', is_print=True):
        url = 'https://emappdata.eastmoney.com/stockrank/getAllCurrentList'
        content_text = {"appId": "appId01", "globalId": "786e4c21-70dc-435a-93bb-38", "pageNo":  self.pageNo,
                        "pageSize": self.pageSize}
        html = self.__post(url, content_text)
        data = json.loads(html)
        secids = ','.join(list(row['sc'].replace('SZ', '0.').replace('SH', '1.') for row in data['data']))

        stock_url = 'https://push2.eastmoney.com/api/qt/ulist.np/get?ut=f057cbcbce2a86e2866ab8877db1d059&fltt=2&invt=2&fields=f14,f148,f3,f12,f2,f13&secids={}' \
            .format(secids)

        if is_print:
            self._get('人气榜', stock_url, fields, is_print)
        else:
            return self._get('人气榜', stock_url, fields, is_print)

    def get_lhb(self, page=1, limit=10, updated='2021-06-23'):
        url = 'https://datacenter.eastmoney.com/securities/api/data/get?type=RPT_DAILYBILLBOARD_DETAILS&sty=ALL&source=DataCenter&client=WAP&p={}&ps={}&sr=-1,1&st=TRADE_DATE,SECURITY_CODE&filter=(TRADE_DATE%3E=%27{}%27)(TRADE_DATE%3C=%27{}%27)&?v={}' \
            .format(page, limit, updated, updated, self._t)
        data = self.__curl(url)
        return data['result']['data']

    def get_me(self):
        url = 'https://myfavor.eastmoney.com/v4/wapouter/gstkinfos?appkey=045986a3ceba181d1fa5309652cd1939&g=1&_=1624254379431'

        headers = {"Content-Type": 'application/json',
                   "Referer": "https://wap.eastmoney.com/",
                   "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1",
                   "Cookie": "qgqp_b_id=fc02c3c5d5757e0ebe013b0d706fbdf8; st_si=84209263837817; HAList=a-sz-300059-%u4E1C%u65B9%u8D22%u5BCC; em_hq_fls=js; wap_ck2=true; ad_tc_221000003503280169=true; st_asi=delete; ct=sMsG5cOnZgRJxVuZD2_tRcyXrZ5gXdPJt9QTVDP0UCeBKG_y0Zc1-2ofo8sCS9-9_GNiZV0DEiM2pBzOvX5taCQai0wtbSykTKeH-KzxsM4h2GVNTjQIhU6LLDz3qa0sXf541mYXfqAop52eXgKjkA9aKEs_rl_f9p8l6Z60BBc; ut=FobyicMgeV4UJna6Au6ASo611uEU66P6lcORe-20kRYhzrJaWyHmvtg9Lu8rWySGIHys9DGA3uES42hfEGU0lL7XQ252U3r9-ys9kLgHkSjbLzv4p4_vWAUKo4KBEwSNbm2QhkIcoBDJBu8sN2fQN0JdvbAMlRRF-iAUIhuQ2QEmgDTD1QCmKcpL15f3bEkY6gQSEoSXPXaXXMAunzP-WUGnGa7LTxg_ahb1hVYpCshvD_VyWMahOoDYLxbEz70cVfG3hXd9oYRBngX4I_aa5rEHTEq9o3o6; pi=3704094407396500%3bm3704094407396500%3b%e4%b8%80%e5%8f%aa%e4%bf%ae%e8%a1%8c%e7%9a%84%e9%b1%bc%3b5xMsLWvtmg%2b%2bYv8kae4hv7gT1GdGTfTJlqnQx0MZdWKXomUbGYD1aWjU%2ba2X7jKsz3bN2C1ebREEBrRhiax%2baCyM1ry2fgUPN0U8Yw5x7fMMX3bEGItoNguhAKVRomeY4lkCnb5GL9tN6BhzrQ1vKjEW7INMmdK9WC6M2Ygy9J3RCgooiDXC8FPGz%2bKIlgJTEdufheVl%3bYxZMCANU00tIiZca2HK8YvhJTpOXl%2fatWWuAvXnonAQgXLNmW3KdggmEmaRuh4n8Kz1t085vCOAVbIgphijU2B7DKfEgnx%2fqLC%2f3z9iqQnqvVfO3FEXVhAqRofxPa7qPJWRNVGoFp%2brYCKr765VqqrpooYzpbA%3d%3d; uidal=3704094407396500%e4%b8%80%e5%8f%aa%e4%bf%ae%e8%a1%8c%e7%9a%84%e9%b1%bc; sid=113949887; vtpst=|; st_pvi=48598162530870; st_sp=2021-04-26%2013%3A34%3A59; st_inirUrl=https%3A%2F%2Fwww.baidu.com%2Flink; st_sn=118; st_psi=20210621134619640-113803310772-1947146732"}

        req = urllib.request.Request(url=url, headers=headers)
        resp = urllib.request.urlopen(req, timeout=10)
        html = resp.read().decode('utf8')
        data = json.loads(html)

        secids = ','.join(list(
            row['security'].split('$')[0] + '.' + row['security'].split('$')[1] for row in data['data']['stkinfolist']))
        stock_url = 'https://push2.eastmoney.com/api/qt/ulist/get?np=1&fltt=2&invt=2&fields=f2,f3,f4,f12,f13,f14,f128&pn={}&pz={}&fid=f3&po=1&secids={}' \
            .format(self.pageNo,self.pageSize,secids)

        self._get('自选', stock_url, 'f14,f12,f2,f3:0:%')

    def get_lhb_buy(self, code='600053', trade_date='2021-09-01', is_print=True):
        url = 'https://datacenter.eastmoney.com/securities/api/data/get?type=RPT_BILLBOARD_DAILYDETAILSBUY&sty=EXPLANATION,CHANGE_TYPE,OPERATEDEPT_CODE,OPERATEDEPT_NAME,TRADE_DATE,NET,BUY,SELL,RISE_PROBABILITY_3DAY,TOTAL_BUYER_SALESTIMES_3DAY,OPERATEDEPT_CODE_OLD&callback=&extraCols=&filter=(SECURITY_CODE=%22{}%22)(TRADE_DATE=%27{}%27)&p=1&ps=200&sr=-1&st=BUY&token=&var=&source=DataCenter&client=WAP&?v={}' \
            .format(code, trade_date, self._t)
        result = self.__curl(url)
        try:
            data = result['result']['data']
        except Exception as e:
            print(result, e)
            return []
        repeat_list = []
        result_data = []
        for row in data:
            if 'BUY' not in row or row['BUY'] == None:
                row['BUY'] = 0
            if 'SELL' not in row or row['SELL'] == None:
                row['SELL'] = 0
            md5 = self.__md5([row['OPERATEDEPT_NAME'], row['OPERATEDEPT_CODE'], row['NET'], row['BUY'], row['SELL']])
            if md5 in repeat_list:
                continue
            if is_print:
                str = '{}|{}|{}|{}|{}' \
                    .format(row['OPERATEDEPT_NAME'].replace('中国', '').replace('证券股份有限公司', '').replace('股份有限公司', ''),
                            row['OPERATEDEPT_CODE'],
                            self._field_type(row['NET'], 4, '万'),
                            self._field_type(row['BUY'], 4, '万'),
                            self._field_type(row['SELL'], 4, '万'))
                repeat_list.append(md5)
                print(str)
            else:
                result_data.append(
                    {'department_code': row['OPERATEDEPT_CODE'].replace('中国', '').replace('证券股份有限公司', '').replace(
                        '股份有限公司', ''),
                     'department_name': row['OPERATEDEPT_NAME'],
                     'net': row['NET'],
                     'buy': row['BUY'],
                     'sell': row['SELL']})

        if is_print != True:
            return result_data

    def get_lhb_sell(self, code='600053', trade_date='2021-09-01', is_print=True):
        url = 'https://datacenter.eastmoney.com/securities/api/data/get?type=RPT_BILLBOARD_DAILYDETAILSSELL&sty=EXPLANATION,CHANGE_TYPE,OPERATEDEPT_CODE,OPERATEDEPT_NAME,TRADE_DATE,NET,BUY,SELL,RISE_PROBABILITY_3DAY,TOTAL_BUYER_SALESTIMES_3DAY,OPERATEDEPT_CODE_OLD&callback=&extraCols=&filter=(SECURITY_CODE=%22{}%22)(TRADE_DATE=%27{}%27)&p=1&ps=200&sr=-1&st=SELL&token=&var=&source=DataCenter&client=WAP&v={}' \
            .format(code, trade_date, self._t)
        result = self.__curl(url)
        try:
            data = result['result']['data']
        except Exception as e:
            print(result, e)
            return []
        repeat_list = []
        result_data = []
        for row in data:
            if 'BUY' not in row or row['BUY'] == None:
                row['BUY'] = 0
            if 'SELL' not in row or row['SELL'] == None:
                row['SELL'] = 0
            md5 = self.__md5([row['OPERATEDEPT_NAME'], row['OPERATEDEPT_CODE'], row['NET'], row['BUY'], row['SELL']])
            if md5 in repeat_list:
                continue
            if is_print:
                str = '{}|{}|{}|{}|{}' \
                    .format(row['OPERATEDEPT_NAME'].replace('中国', '').replace('证券股份有限公司', '').replace('股份有限公司', ''),
                            row['OPERATEDEPT_CODE'],
                            self._field_type(row['NET'], 4, '万'),
                            self._field_type(row['BUY'], 4, '万'),
                            self._field_type(row['SELL'], 4, '万'))
                repeat_list.append(md5)
                print(str)
            else:
                result_data.append({'department_code': row['OPERATEDEPT_CODE'].replace('中国', '').replace('证券股份有限公司',
                                                                                                         '').replace(
                    '股份有限公司', ''),
                                    'department_name': row['OPERATEDEPT_NAME'],
                                    'net': row['NET'],
                                    'buy': row['BUY'],
                                    'sell': row['SELL']})

        if is_print != True:
            return result_data

    def get_lottery(self, name = 'ssq',issueCount = 1, is_print = True):
        #3d
        url = 'http://www.cwl.gov.cn/cwl_admin/front/cwlkj/search/kjxx/findDrawNotice?name={}&issueCount={}&issueStart=&issueEnd=&dayStart=&dayEnd=' \
            .format(name,issueCount)
        res = requests.get(url,headers={}, timeout=30)
        html = res.content
        data = json.loads(html)
        if data['state'] == 0:
            result = []
            for i in data['result']:
                red_list = i['red'].split(',')
                item = {}
                item['type'] = name
                item['name'] = i['name']
                item['code'] = i['code']
                item['date'] = i['date'][0:10]
                item['week'] = i['week']
                item['red1'] = int(red_list[0])
                item['red2'] = int(red_list[1])
                item['red3'] = int(red_list[2])
                item['red4'] = int(red_list[3])
                item['red5'] = int(red_list[4])
                item['red6'] = int(red_list[5])
                item['blue1'] = int(i['blue'])
                item['blue2'] = 0 if i['blue2'] == '' else i['blue2']
                result.append(item)
            if is_print:
                for row in result:
                    print("{}|{}|{}|{}|{},{},{},{},{},{}|{}".format(
                        row['name'],
                        row['code'],
                        row['date'],
                        row['week'],
                        row['red1'],
                        row['red2'],
                        row['red3'],
                        row['red4'],
                        row['red5'],
                        row['red6'],
                        row['blue1']
                    ))
            else:
                return result
        else:
            return False

    def __post(self, url, content_text):
        data = json.dumps(content_text)
        data = bytes(data, 'utf8')
        headers = {"Content-Type": 'application/json'}
        req = urllib.request.Request(url=url, headers=headers, data=data)
        resp = urllib.request.urlopen(req, timeout=10)
        return resp.read().decode('utf8')

    def _get(self, tags, url, fields, is_print=True):
        print('{}----------'.format(tags))
        data = self.__curl(url)
        data_list = data['data']['diff'];
        result = []
        for row in data_list:
            if type(row) == str:
                row = data_list[row]

            if fields == '':
                item = row
            else:
                item = self._field(fields, row)
            result.append(item)

        if is_print:
            self.dump(result)
        else:
            return result

    def dump(self, data, tags=''):
        if len(tags) > 0:
            print('{}----------'.format(tags))
        # data = data[::-1]
        for row in data:
            if type(row) != list:
                print('|'.join(str(i) for i in data))
                return
            print('|'.join(str(i) for i in row))

    def _field_type(self, val, val_type, tags='%'):
        if type(val) == float or type(val) == int:
            if val_type > 0:
                if val_type == 3:
                    quantize_str = '0.000'
                else:
                    quantize_str = '0.00'

                val = '{}{}'.format(decimal.Decimal(val / (10 ** val_type) ).quantize(decimal.Decimal(quantize_str)), tags)
            else:
                val = '{}{}'.format(val, tags)
        return val

    def _field(self, fields, data):
        if fields == '':
            return data
        item = []
        fields_list = fields.split(',')
        for field_str in fields_list:
            field_data = field_str.split(':')
            field = field_data[0]
            try:
                field_type = int(field_data[1])
            except Exception as e:
                field_type = -1
            try:
                field_tags = str(field_data[2])
            except Exception as e:
                field_tags = ''
            val = data[field]
            if field == 'f6' or field == 'f62':
                val = self._field_type(val, 8, '亿')
            else:
                val = self._field_type(val, field_type, field_tags)

            item.append(val)
        return item

    def __curl_old(self, url):
        attempt = 0
        retries = 3
        while attempt < retries:
            try:
                res = urllib.request.urlopen(url, timeout=30)
                html = res.read().decode('utf8')
                data = json.loads(html)
                return data
            except Exception as e:
                print(e)
                attempt += 1

    def init_browser(self):

        CHROME_PORT = 10002

        co = ChromiumOptions().set_paths(local_port=CHROME_PORT)

        # if SPIDER_ENV == 'dev':
        #     proxy_ip = '127.0.0.1:10809'
        # elif SPIDER_ENV == 'prod':
        #     proxy_ip = get_proxy()
        #
        # co.set_proxy('http://{}'.format(proxy_ip))

        # 无头模式
        co.set_argument("--headless")
        # 无痕模式
        co.set_argument("--incognito")
        # 禁用密码保存提示
        co.set_argument("--disable-save-password-bubble")
        # 禁用信息栏
        # co.set_argument("--disable-infobars")
        # 禁用插件和扩展
        co.set_argument("--disable-plugins-discovery")
        co.set_argument("--disable-extensions")
        # 禁用GPU加速
        co.set_argument("--disable-gpu")
        # 关闭沙盒模式
        co.set_argument("--disable-sandbox")
        co.set_argument("--disable-dev-shm-usage")

        # 用该配置创建页面对象
        self.browser = ChromiumPage(addr_driver_opts=co)

    def __curl(self, url):
        return self.__curl_old(url)
        self.init_browser()
        self.browser.get(url)
        return self.browser.json

    # 处理MD5
    def __md5(self, data):
        m = hashlib.md5()
        m.update(str(data).encode(encoding='UTF-8'))
        return m.hexdigest()

