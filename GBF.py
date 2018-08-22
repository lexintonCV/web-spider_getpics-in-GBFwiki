import requests
from bs4 import BeautifulSoup
import re
import os
import time


class bf():
    def __init__(self):
        self.url_main = "https://gbf.huijiwiki.com"
        self.url_class = ["https://gbf.huijiwiki.com/wiki/SSR%E4%BA%BA%E7%89%A9",
                          "https://gbf.huijiwiki.com/wiki/SR%E4%BA%BA%E7%89%A9",
                          "https://gbf.huijiwiki.com/wiki/SSR%E5%8F%AC%E5%94%A4%E7%9F%B3",
                          "https://gbf.huijiwiki.com/wiki/R%E4%BA%BA%E7%89%A9"]
        self.headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"}

    def getHTMLText(self, url):
        content = requests.get(url, headers=self.headers)
        return content.text
        
    def getRoleUrl(self):
        html = self.getHTMLText(self.url_class[0])
        bs = BeautifulSoup(html, 'html.parser')
        all_table = bs.find_all('table')
        all_a = []
        for table in all_table:
            a = table.find_all('a')
            all_a = all_a+a
            all_a_herf = []
        for a in all_a:
            all_a_herf.append(a['href'])
            l2 = []
            [l2.append(i) for i in all_a_herf if not i in l2]
        return l2
        
    def getPic(self,all_a_href):
        i=0
        os.chdir('F:/pic_pc/1')
        for href in all_a_href:
            url = self.url_main+href
            html = self.getHTMLText(url)
            bs = BeautifulSoup(html,'html.parser')
            title = bs.title
            all_li = bs.find_all('li',class_ = 'gallerybox')
            for li in all_li:
                i=i+1
                all_img = li.find_all('img')
                for src in all_img:
                    pic_url = src['src'].replace('450px','900px').replace('358px','716px')
                    print(pic_url)
                    pic = requests.get(pic_url, headers=self.headers)
                    name = i
                    img = pic.content
                    self.downloadPic(img,name)
                    
    def downloadPic(self,img,name):
        name= str(name)
        print('正在保存名字为: ' + name + ' 的图片')
        with open(name + '.png', 'ab') as f:  # 图片要用b
            f.write(img)
            f.close()
        print('保存该图片完毕')
        time.sleep(5)
        
    def mkdir(self, path):
        path = path.strip()
        isExists = os.path.exists(os.path.join("F:\pic_pc", path))
        if not isExists:
            print(u'建了一个名字叫做', path, u'的文件夹！')
            os.makedirs(os.path.join("F:\pic_pc", path))
            return True
        else:
            print(u'名字叫做', path, u'的文件夹已经存在了！')
            return False
            
    def main():
        a = bf()
        a.mkdir('1')
        c= a.getPic(a.getRoleUrl())
        
main()
