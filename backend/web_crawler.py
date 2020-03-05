#!/bin/usr/env python3
# -*- coding: utf-8 -*-

# 爬取网站资源

__author__ = 'mask'

import urllib.request
import re
import os
import time
from functools import reduce

IMG_TYPE_ARR = ['jpg', 'png', 'ico', 'gif', 'jpeg', 'svg']

# 正则表达式预编译
# 这里涉及到了非贪婪匹配
# ((?:/[a-zA-Z0-9.]*?)*)
# ((?:/[a-zA-Z0-9.]*)*?)
REG_URL = r'^(https?://|//)?((?:[a-zA-Z0-9-_]+\.)+(?:[a-zA-Z0-9-_:]+))((?:/[-_.a-zA-Z0-9]*?)*)((?<=/)[-a-zA-Z0-9]+(?:\.([a-zA-Z0-9]+))+)?((?:\?[a-zA-Z0-9%&=]*)*)$'
REG_RESOURCE_TYPE = r'(?:href|src|data\-original|data\-src)=["\'](.+?\.(?:js|css|jpg|jpeg|png|gif|svg|ico|ttf|woff2))[a-zA-Z0-9\?\=\.]*["\']'

regUrl = re.compile(REG_URL)
regResouce = re.compile(REG_RESOURCE_TYPE, re.S)


# "" or ''
# ?: 取消分组
# ?表示懒惰匹配，尽可能匹配少的字符
'https://blog.csdn.net/pythonniu/article/details/51855035/a.c/aaa.html'
'https://csdnimg.cn/release/blog_editor_html/release1.3.1/ckeditor/plugins/chart/lib/chart.min.js'
'http://www.xinchain.org/'
'//abc.com'
'http://192.168.1.109:8080/abc/images/111/index.html?a=1&b=2'
'https://pixabay.com/zh/editors_choice/?media_type=photo&pagi=4'
'http://www.imooc.com/'
'https://www.vip.com/'
'http://www.xinchain.org/'
'http://192.168.1.109:8080/abc/images/111/index.html?a=1&b=2'
'http://www.jd.com/index.htm'
'https://blog.csdn.net/pythonniu/article/details/51855035'
'https://segmentfault.com/'
'https://github.com/'
url = 'http://www.lizhizu.com/channel'

SAVE_PATH = os.path.join(os.path.abspath('.'), 'python-spider-downloads')

downloadedList = []

'''
解析URL地址
'''
def parseUrl(url):
    if not url:
        return

    res = regUrl.search(url)
    # 在这里，我们把192.168.1.109:8080的形式也解析成域名domain，实际过程中www.baidu.com等才是域名，192.168.1.109只是IP地址
    # ('http://', '192.168.1.109:8080', '/abc/images/111/', 'index.html', 'html', '?a=1&b=2')
    if res is not None:
        path = res.group(3)
        fullPath = res.group(1) + res.group(2) + res.group(3)

        if not path.endswith('/'):
            path = path + '/'
            fullPath = fullPath + '/'
        return dict(
            baseUrl=res.group(1) + res.group(2),
            fullPath=fullPath,
            protocol=res.group(1),
            domain=res.group(2),
            path=path,
            fileName=res.group(4),
            ext=res.group(5),
            params=res.group(6)
        )


def isCssType(str):
    return str.lower().endswith('.css')


def isJsType(str):
    return str.lower().endswith('.js')


def isImgType(str):
    for ext in IMG_TYPE_ARR:
        if str.endswith('.' + ext):
            return True


def splitResourceType(list):
    jsList = []
    cssList = []
    imgList = []

    for s in list:
        if isImgType(s):
            imgList.append(s)
        elif isCssType(s):
            cssList.append(s)
        elif isJsType(s):
            jsList.append(s)
        else:
            print('什么类型也不是，解析资源出错！！！：', s)

    return jsList, cssList, imgList


'''
下载文件
'''
def downloadFile(srcPath, distPath):
    global downloadedList

    if distPath in downloadedList:
        return
    try:
        response = urllib.request.urlopen(srcPath)
        if response is None or response.status != 200:
            return print('> 请求异常：', srcPath)
        data = response.read()

        f = open(distPath, 'wb')
        f.write(data)
        f.close()

        downloadedList.append(distPath)
        # print('>>>: ' + srcPath + '：下载成功')

    except Exception as e:
        print('报错了：', e)


'''
解析路径

eg:
    basePath => F:\Programs\python\python-spider-downloads
    resourcePath => /a/b/c/ or a/b/c

    return => F:\Programs\python\python-spider-downloads\a\b\c
'''
def resolvePath(basePath, resourcePath):
    # 解析资源路径
    res = resourcePath.split('/')
    # 去掉空目录 /a/b/c/ => [a, b, c]
    dirList = list(filter(lambda x: x, res))

    # 目录不为空
    if dirList:
        # 拼接出绝对路径
        resourcePath = reduce(lambda x, y: os.path.join(x, y), dirList)
        dirStr = os.path.join(basePath, resourcePath)
    else:
        dirStr = basePath

    return dirStr


def main():
    global SAVE_PATH
    # 首先创建这个站点的文件夹
    urlDict = parseUrl(url)
    print('分析的域名：', urlDict)
    domain = urlDict['domain']

    filePath = time.strftime('%Y-%m-%d', time.localtime()) + '-' + domain
    # 如果是192.168.1.1:8000等形式，变成192.168.1.1-8000，:不可以出现在文件名中
    filePath = re.sub(r':', '-', filePath)
    SAVE_PATH = os.path.join(SAVE_PATH, filePath)

    # 读取网页内容
    webPage = urllib.request.urlopen(url)
    data = webPage.read()
    content = data.decode('UTF-8')
    print('> 网站内容抓取完毕，内容长度：', len(content))

    # 把网站的内容写下来
    pageName = ''
    if urlDict['fileName'] is None:
        pageName = 'index.html'
    else:
        pageName = urlDict['fileName']

    pageIndexDir = resolvePath(SAVE_PATH, urlDict['path'])
    if not os.path.exists(pageIndexDir):
        os.makedirs(pageIndexDir)

    pageIndexPath = os.path.join(pageIndexDir, pageName)
    print('主页的地址:', pageIndexPath)
    f = open(pageIndexPath, 'wb')
    f.write(data)
    f.close()

    # 解析网页内容，获取有效的链接
    contentList = re.split(r'\s+', content)
    resourceList = []
    for line in contentList:
        resList = regResouce.findall(line)
        if resList is not None:
            resourceList = resourceList + resList

    # 对资源进行分组，从而可以下载特定的资源
    (jsList, cssList, imgList) = splitResourceType(resourceList)

    # 下载资源，要区分目录，不存在的话就创建
    for resourceUrl in resourceList:
        # ./static/js/index.js
        # /static/js/index.js
        # static/js/index.js
        # //abc.cc/static/js
        # http://www.baidu/com/static/index.js
        if resourceUrl.startswith('./'):
            resourceUrl = urlDict['fullPath'] + resourceUrl[1:]
        elif resourceUrl.startswith('//'):
            resourceUrl = 'https:' + resourceUrl
        elif resourceUrl.startswith('/'):
            resourceUrl = urlDict['baseUrl'] + resourceUrl
        elif resourceUrl.startswith('http') or resourceUrl.startswith('https'):
            # 不处理，这是我们想要的url格式
            pass
        elif not (resourceUrl.startswith('http') or resourceUrl.startswith('https')):
            # static/js/index.js这种情况
            resourceUrl = urlDict['fullPath'] + resourceUrl
        else:
            print('> 未知resource url: %s' % resourceUrl)

        # 解析文件，查看文件路径
        resourceUrlDict = parseUrl(resourceUrl)
        if resourceUrlDict is None:
            print('> 解析文件出错：%s' % resourceUrl)
            continue

        resourceDomain = resourceUrlDict['domain']
        resourcePath = resourceUrlDict['path']
        resourceName = resourceUrlDict['fileName']

        if resourceDomain != domain:
            print('> 该资源不是本网站的，也下载：', resourceDomain)
            # 如果下载的话，根目录就要变了
            # 再创建一个目录，用于保存其他地方的资源
            resourceDomain =  re.sub(r':', '-', resourceDomain)
            savePath = os.path.join(SAVE_PATH, resourceDomain)
            if not os.path.exists(SAVE_PATH):
                print('> 目标目录不存在，创建：', savePath)
                os.makedirs(savePath)
            # continue
        else:
            savePath = SAVE_PATH

        # 解析资源路径
        dirStr = resolvePath(savePath, resourcePath)

        if not os.path.exists(dirStr):
            print('> 目标目录不存在，创建：', dirStr)
            os.makedirs(dirStr)

        # 写入文件
        downloadFile(resourceUrl, os.path.join(dirStr, resourceName))

    print('-----------------下载完成------------------')
    print('总共下载了%d个资源' % len(downloadedList))


if __name__ == '__main__':
    main()
    pass
