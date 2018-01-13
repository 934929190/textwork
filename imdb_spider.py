#coding=utf-8

from scrapy.spiders import Spider
from scrapy.http import Request
from scrapy.selector import Selector #原文里的HtmlXpathSelector全部换成了Selector
from tutorial.items import TutorialItem
import re
import urllib

class ImdbSpider(Spider):
    name = "imdb"
    allowed_domains = ["www.imdb.com"]
    start_urls = []

    def start_requests(self):
        file_object = open('movie_name.txt','r')  #电影名存储在movie_name.txt文件里

        try: 
            url_head = "http://www.imdb.com/find?ref_=nv_sr_fn&q="  #imdb电影搜索的url头
            for line in file_object:
                self.start_urls.append(url_head + line + '&s=tt')
                #&s=tt是限定搜索仅限标题，可以过滤掉电影名正好是影人名导致爬到影人照片的情况

            for url in self.start_urls:
                yield self.make_requests_from_url(url)
        finally:
            file_object.close()

    def parse(self, response):
        #open("test.html",'wb').write(response.body)#测试response是否正确

        hxs = Selector(response)
        #为了防止爬到空白图片（如缺少海报的电影或者TV Series），加一个循环，遇到空白预览图往下搜
        i = 1
        movie_pic = hxs.xpath('id("main")/div/div[2]/table/tr[1]/td[1]/a/img/@src').extract()
        while movie_pic[0].find('nopicture') == -1:
            i++
            movie_pic = hxs.xpath('id("main")/div/div[2]/table/tr[%d]/td[1]/a/img/@src' % i).extract()
            #如果是所有的结果都没有预览图的情况，还是要跳出循环的
            if not movie_pic:
                break
        #open("movie_pic.txt", 'w').write(str(movie_pic))#测试海报url是否正确

        #为了减少request量，这里使用了一个偷懒的方法：
        #因为imdb搜索结果页的海报预览图和电影具体信息页面的海报预览图在url上只有表示尺寸值的字符串差别，
        #所以这里直接替换，就不需要从@href的链接访问进去了。如果需要更大的海报，到相应的页面去找，可以发现只要把
        #“UX182_CR0,0,32,44_AL_.jpg”换成“SX640_SY720_.jpg”就行了
        if movie_pic:
            movie_pic[0]=movie_pic[0].replace('32','182')
            movie_pic[0]=movie_pic[0].replace('44','268')

        #下载海报预览图
        item = TutorialItem()
        item['movie_picture'] = ''.join(movie_pic).strip()
        movie_name_file = open('movie_name.txt','r')
        try:
            for line in movie_name_file:
                item['movie_name'] = line.strip()
                if movie_pic:
                    urllib.urlretrieve(movie_pic[0].strip(),'pictures/' + line.strip() + '.jpg')
        finally:
            movie_name_file.close()
      yield item
