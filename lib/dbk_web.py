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
from lxml import etree

class dbk_web(object):

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

    # 获取
    def day_time(self, day='20240902'):
        url = 'https://www.dabanke.com/index-{}.html'.format(day)
        html = self.__curl_old(url)
        xpath = etree.HTML(html)
        data = {
            'status' : False,
            'msg' : '',
            'data' : []
        }
        msg = xpath.xpath("//*[contains(@class, 'card-body')]/p/text()")[0]
        if '非交易日' in msg:
            data['msg'] = '非交易日'
        else:
            data['status'] = True
            data['msg'] = '交易日'
        trs = xpath.xpath("//html/body/div/div[6]/table/tbody/tr")
        for tr in trs:
            info = {}
            info['top'] = tr.xpath('./td[1]/text()')[0].strip()
            info['msg'] = tr.xpath('./td[2]/text()')[0].strip()
            info['info'] = []
            info_items = tr.xpath('./td[3]/div/div')
            for info_item in info_items:
                row_tmp = [i.strip() for i in info_item.xpath('.//span//text()')]
                code = info_item.xpath('.//a/@href')[0][8:14]
                row = {
                    'market' : row_tmp[0].strip(),
                    'name' : row_tmp[2].strip(),
                    'code' : code,
                    'is_t0' : row_tmp[4].strip().replace('(','').replace(')',''),
                    'rate' : row_tmp[5].strip(),
                    'bk_name' : row_tmp[6].strip()
                }
                info['info'].append(row)
            data['data'].append(info)
        return data

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
        response = requests.get(url, timeout=30,verify=False)
        data = response.text
        return data

    def init_browser(self):

        CHROME_PORT = 10001

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
        self.init_browser()
        self.browser.get(url)
        return self.browser.json

    # 处理MD5
    def __md5(self, data):
        m = hashlib.md5()
        m.update(str(data).encode(encoding='UTF-8'))
        return m.hexdigest()

