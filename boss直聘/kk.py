import requests
import re
import json
import execjs
import ssl
from bs4 import BeautifulSoup

ssl._create_default_https_context = ssl._create_unverified_context

from urllib.parse import unquote

allDaili={'http': '59.60.120.201:27172'}
def getTiaoZhuanLocation():
    url='https://www.zhipin.com/c100010000-p100120/'

    headerss = {
"authority": "www.zhipin.com",
"scheme": "https",
"path": "/c100010000-p100120/",
"upgrade-insecure-requests": "1",
"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36",
"accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
"sec-fetch-site": "none",
"sec-fetch-mode": "navigate",
"sec-fetch-dest": "document",
"accept-encoding": "gzip, deflate, br",
"accept-language": "zh-CN,zh;q=0.9"
                }
    proxies = {'http': '127.0.0.1:8888'}
    r = requests.get(url.replace('https', 'https'), headers=headerss, timeout=10, allow_redirects=False,verify=False)
    print(r.status_code)
    print(r.headers.get('location'))
    return r.headers.get('location')

#正则获取关键数据
def g(patternStr,urlInfo):
   # searchObj = re.search("(^|&)" + patternStr + "=([^&]*)(&|$)", urlInfo)
    ss=re.findall(patternStr+"=(.+?)&", urlInfo)
    print(ss)
    return ss

def get302UrlInfo(urlInfo):
    headers = {
        "authority": "www.zhipin.com",
        "scheme": "https",
        "path": "/web/common/security-js/1f49f5f3.js",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36",
        "accept": "*/*",
        "sec-fetch-site": "same-origin",
        "sec-fetch-mode": "no-cors",
        "sec-fetch-dest": "script",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9"

    }
    proxies = {'https': '127.0.0.1:8888'}
    url = "https://www.zhipin.com"+urlInfo

    r = requests.get(url, timeout=10,  allow_redirects=False, verify=False)



def getCookie(urlInfo):
    #访问返回参数集
   # get302UrlInfo(urlInfo)

    #正常操作，获取关键数据

    print()
    print(urlInfo)
    n = g("name", urlInfo)
    jsTXt=getJsTxt(n[0])

    #合成js算法







    pingJieJs='function  zhixing(jiaMiTxt,canshu) { \n'\
            'const jsdom1 = require("/usr/local/lib/node_modules/jsdom"); \n'\
            'const {JSDOM} = jsdom1; \n'\
            "dom = new JSDOM(`<!DOCTYPE html><html></html>`,{url: 'https://www.zhipin.com'}); \n "\
            'window={};window=dom.window;navigator=window.navigator;document=window.document; \n '\
            'location={"href": "https://www.zhipin.com"+canshu, "ancestorOrigins": {}, "origin": "https://www.zhipin.com", "protocol": "https:", "host": "www.zhipin.com", "hostname": "www.zhipin.com", "port": "", "pathname": "/web/common/security-check.html", "search": canshu.replace("/web/common/security-check.html",""), "hash": ""} ;\n'\
              'top=window; \n'\
                'var b = new RegExp("(^|&)seed=([^&]*)(&|$)");'\
                'canshu0 = location.search.substr(1).match(b)[2];'\
                    'canshu0=decodeURIComponent(canshu0);'\
                    'var b = new RegExp("(^|&)ts=([^&]*)(&|$)");'\
            'canshu1 = location.search.substr(1).match(b)[2];'\
            'window.eval(jiaMiTxt); \n'\
            'g = global.ABC ;\n'\
            "d = (new g).z(canshu0, parseInt(canshu1) + 1000 * 60 * (480 + (new Date).getTimezoneOffset())); \n"\
            "return encodeURIComponent(d);}"

    #ceshiNode(jsTXt, locationString, canshu0, canshu1)
    ctx = execjs.compile(pingJieJs)
    jj=ctx.call("zhixing",jsTXt,urlInfo)
    print(jj)
    print('-------------')
    getInfo(jj,urlInfo)

   # print(pingJieJs)


def getInfo(cookieValue,houzhui):
    url = 'https://www.zhipin.com/c100010000-p100120/'

    headerss = {
        "upgrade-insecure-requests": "1",
"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36",
"accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
"sec-fetch-site": "same-origin",
"sec-fetch-mode": "navigate",
"sec-fetch-dest": "document",
"referer": "https://www.zhipin.com"+houzhui,
"accept-encoding": "gzip, deflate, br",
"accept-language": "zh-CN,zh;q=0.9",
"cookie": "__zp_stoken__="+cookieValue
    }
    proxies = {'http': '127.0.0.1:8888'}
    r = requests.get(url.replace('https', 'https'), headers=headerss,  timeout=10,
                     allow_redirects=False, verify=False)
    print(r.status_code)
    if(r.status_code==200):
        jieXiHtml(r.text)
    else:
        #判断是否出现人机验证
        returnLocation=r.headers.get('location')
        if(str(returnLocation).__contains__('sliderNew')):
            print('出现人机验证')
        else:
            print('尝试再运行一次')

def jieXiHtml(htmlTxt):
    soup = BeautifulSoup(htmlTxt)
    htmlLiList=soup.select('#main > div > div.job-list > ul > li')
    for htmlli in htmlLiList:
        print(htmlli.select_one('.job-name').get_text())
        print(htmlli.select_one('.job-area-wrapper').get_text())


    print()

def ceshiNode(jsTXt,locationString,canshu0,canshu1):

    url = 'http://0.0.0.0:3000/boss?'

    r = requests.post(url, data={'jsTXt': jsTXt, 'locationString': locationString,'canshu0':canshu0,'canshu1':canshu1})
    print(r.status_code)

#获取js，采用url获取，后期可变为存入本地数据库
def getJsTxt(jsBiaoShi):
    headers={
        "authority": "www.zhipin.com",
    "scheme": "https",
    "path": "/web/common/security-js/1f49f5f3.js",
   "user-agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36",
    "accept": "*/*",
    "sec-fetch-site": "same-origin",
    "sec-fetch-mode": "no-cors",
    "sec-fetch-dest": "script",
    "accept-encoding": "gzip, deflate, br",
    "accept-language":"zh-CN,zh;q=0.9"

    }
    proxies = {'https': '127.0.0.1:8888'}

    url='https://www.zhipin.com/web/common/security-js/'+str(jsBiaoShi)+'.js'
    r = requests.get(url, timeout=10, allow_redirects=False,verify=False)
    print(r.text)
    return r.text

if __name__ == '__main__':

    getCookie(getTiaoZhuanLocation())