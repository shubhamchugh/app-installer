# coding=utf-8

import re

import requests
from pyquery import PyQuery
from requests.exceptions import RequestException

DEBUG = False
User_Agent = ('Mozilla/5.0 (Windows NT 6.1; WOW64)'
              ' AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36')

KUAN_URL = 'https://www.coolapk.com/apk/'

APKPURE_BASE = 'https://apkpure.com'
APKPURE_SEARCH = 'https://apkpure.com/cn/search?q='
APKPURE_DOWNLOAD = 'https://apkpure.com{}/download?from=details'


def kuan(pkg):
    """
    从 www.coolapk.com 下载app
    :param  pkg: apk包名
    """
    # 酷安网必须要使用同一个session发起请求，而不能使用多次requests.get函数
    with requests.Session() as ss:
        headers = {}
        headers['User-Agent'] = User_Agent
        resp = ss.get(url=KUAN_URL+pkg, headers=headers)
        if not resp.ok:
            raise RequestException(resp.status_code, resp.reason)
        pq = PyQuery(resp.text)
        onDownloadApk = pq('body>script').eq(0).text()
        if DEBUG:
            print('kuan: onDownloadApk', onDownloadApk)
        app_url = re.search(
            r'https://dl\.coolapk\.com/down\?pn={app_name}&id=.*?&from=click'.format(app_name=pkg), onDownloadApk).group()
        headers['Referer'] = KUAN_URL+pkg
        with ss.get(app_url, headers=headers, stream=True) as resp:
            if DEBUG:
                print('kuan: http status code', resp.status_code)
                print('kuan: apk link', resp.url)
            with open(pkg+'.apk', 'wb') as app:
                print('正在从酷安网下载', pkg)
                for i in resp.iter_content(10240):
                    app.write(i)
                print('下载完毕', pkg)


def apkpure(pkg):
    """
    从 apkpure.com 下载app
    :param  pkg: apk包名
    """
    headers = {}
    headers['User-Agent'] = User_Agent
    pq = PyQuery(url=APKPURE_SEARCH+pkg)
    # eg. /cn/shadowsocks/cn.android.shadowsocks
    app_path = pq(
        '#search-res > dl:first-child > dd > p.search-title > a').attr('href')
    if DEBUG:
        print('apkpure: app_path', app_path)
    headers['Referer'] = APKPURE_BASE+app_path
    pq = PyQuery(url=APKPURE_DOWNLOAD.format(app_path))
    app_download = pq('#download_link').attr('href')
    print('正在从apkpure下载', pkg)
    with requests.get(app_download, stream=True) as resp:
        with open(pkg+'.apk', 'wb') as file:
            for i in resp.iter_content(10240):
                file.write(i)
    print('下载完毕', pkg)


def down(pkg):
    try:
        kuan(pkg)
    except Exception as err:
        print('无法从酷安网下载', pkg)
        if DEBUG:
            print(err)
        try:
            apkpure(pkg)
        except Exception as err:
            if DEBUG:
                print(err)
            return False
    return True
