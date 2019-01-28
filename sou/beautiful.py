import requests
import re
import urllib
import os
from bs4 import BeautifulSoup
from urllib.parse import urlparse

def get_html(url):
    """这个函数作用抓取url的内容（二进制内容，可以直接传进beautifulsoup）
       尽量模拟真实的浏览器Referer和User-Agent等）
    """
    try:
        par=urlparse(url)
        Default_Header = {'X-Requested-With': 'XMLHttpRequest',
                          'Referer': par[0] + '://' + par[1],
                          'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.87 Safari/537.36',
                          'Host': par[1]}
        html=requests.get(url,headers=Default_Header,timeout=10)
        return html.content
        if html.status_code!=200:
            return None
    except Exception as e:
        print(e)
        return None
def full_link(url1,url2,flag_site=True):
    """因为宽度优先先要想让while运转起来，就需要对队列的每一个元素
       都有一个通用的处理方法，它的作用是对已知url1里的内容由一个<a>标签
       的href属性里是url2，返回url2真正的完整连接是什么
    """
    try:
        if url2[0]=="#":
            return None
        filepat = re.compile(r'(.*?)\.(.*?)')
        htmpat = re.compile(r'(.*?)\.htm$|(.*?)\.html$|(.*?)\.php$|(.*?)\.aspx$')
        u1 = urlparse(url1)
        if filepat.match(u1.path) and not htmpat.match(u1.path):
            return None
        if url1[-1] == '/':
            url1 = url1 + "index.html"
        elif filepat.match(u1.path) is None:
            url1 = url1 + "/index.html"
        url2 = urllib.parse.urljoin(url1, url2)
        u2 = urlparse(url2)
        if u1.netloc != u2.netloc and flag_site:
            return None
        return url2
    except Exception as e:
        print(e)
        return None
def premake(url):
    """这个函数是建立url所需要的本地文件夹，这一步主要是为了在本地保存原始目录结构。
       而且query 的信息文件名体现出来了
    """
    if url[-1]=='/':
        up=urlparse(url)
    pat = re.compile(r'(.*?)\.htm$|(.*?)\.html$|(.*?)\.php$|(.*?)\.aspx$')
    path=up.path.split('/')
    name='index.html'
    if pat.match(up.path) is not None:
        name=path[-1]
        path=path[:-1]
    dirn='/'.join(path)
    if up.query != '':
        name = up.query + ' - ' + name
    os.makedirs(up.netloc + dirn, exist_ok=True)
    return up.netloc + dirn + '/' + name
def save(url):
    url = url.replace('\n','')
    fn = premake(url)
    html = get_html(url)
    if html is not None:
        with open(fn, 'wb') as f:
            f.write(html)
    return html


if __name__ == '__main__':
    url='https://www.iqiyi.com/w_19rsvnvnt1.html'
    get_html(url)