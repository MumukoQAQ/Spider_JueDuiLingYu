import requests as rs
import re
import lxml.etree as le
import os
import time
class Pc():
    def __init__(self):
        self.url=''
        self.headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'}

    def url_text(self,url,headers):
        '''
        获取网页源代码
        '''
        connect=rs.get(url,headers=headers).text
        html=le.HTML(connect)
        return html

    def mt_info(self,connect):
        '''
        获取模特主页url
        '''
        home_page=connect.xpath('//*[@id="post-list"]/ul/li/div/div/a/@href')
        return home_page

    def get_img_url(self,url):
        '''
        获取模特主页照片url
        '''
        html=self.url_text(url,self.headers)
        img_url=html.xpath('//*[@class="entry-content"]/div/p/img/@src')
        img_url2=html.xpath('//*[@id="primary-home"]/article/div[2]/p/img/@src') #有一些图片链接规则不一样，要两个xpath抓取，否则会漏
        for i in img_url2:
            if img not in img_url:
                img_url.append(i)
        return img_url

    def get_mt_name(self):
        '''
        获取模特名字,由于模特主页有些没名字，就统一用封面名字，因此url不需要传参
        '''
        html = self.url_text(url=self.url, headers=self.headers)
        mt_name=html.xpath('//*[@class="post-info"]/h2/a/text()')
        return mt_name
    def img_get(self,url,filename,c):
        '''
        下载图片到本地
        '''
        down=rs.get(url).content
        if not os.path.exists(r'D:/'+cut+'/'+filename):
            os.mkdir(r'D:/'+cut+'/'+filename)
        path=r'D:/'+cut+'/'+filename+'/'+str(c)+'.jpg'
        with open(path,'wb') as f:
            f.write(down)
            time.sleep(0.1)
            print('正在下载:%s,当前是第%s张'%(filename,c))

Run=Pc()

type=int(input('请输入你要下载的类型\nvlp图请输入: 1\ncosplay图请输入: 2\n妹子图请输入: 3\n二次元图请输入: 4'))

cut=''
if type==1:
    cut='fuli'
elif type==2:
    cut='cosplay'
elif type==3:
    cut='meizi'
else:
    cut='mantu'

page=int(input('请输入你要下载到的页数:'))
if not os.path.exists('D:/'+cut):
    os.mkdir('D:/'+cut)

for i in range(1,page+1):
    Run.url='https://www.jder.net/{}/page/{}'.format(cut,str(i))
    html=Run.url_text(Run.url,Run.headers)
    home_page_url=Run.mt_info(html)
    mt_name=Run.get_mt_name()
    count = 0

    for img in home_page_url:
        count += 1
        c=1
        img_url=Run.get_img_url(img)
        for url in img_url:
            Run.img_get(url,mt_name[count-1].replace(':','：').replace('/',''),c)  #mt_name[count-1] 是文件夹名，有些带有特殊字符，创建文件夹时会报错，所以替换掉
            c += 1





