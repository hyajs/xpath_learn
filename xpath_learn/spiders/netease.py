import scrapy
from selenium import webdriver
from bs4 import BeautifulSoup

class NeteaseSpider(scrapy.Spider):
    name = 'netease'
    allowed_domain = ['fund.eastmoney.com']
    start_urls = ['http://fund.eastmoney.com/manager/default.html#dt14;mcreturnjson;ftall;pn2279;pi1;scabbname;stasc']


    def __init__(self):
        #实例化一个浏览器对象(实例化一次)
        self.bro = webdriver.Chrome()

    #必须在整个爬虫结束后，关闭浏览器
    def closed(self,spider):
        print('爬虫结束')
        self.bro.quit()


    def parse(self, response):

        bs = BeautifulSoup(response.text,'html.parser')
        node_list = bs.find('div',class_ = 'datatable').find('tbody').find_all('tr')
        for node in node_list:
            url = 'http:'+ str(node.find('a')['href'])

            accumulated_work_time = response.xpath('/html/body/div[6]/div[2]/div[2]/div[3]/table/tbody/tr[1]/td[5]/text()').extract()  #收集基金经理累计工作时间
            yield scrapy.Request(url,callback = self.fund_manager_parser,meta={'middleware':'XpathLearnDownloaderMiddleware','accumulated_work_time':accumulated_work_time,'url':url})


    def fund_manager_parser(self,response):
        item = {}
        revenue = []
        bs = BeautifulSoup(response.text,'html.parser')
        item['manager_name'] = bs.find('div',class_='content_in').find('span',class_='left').text  #收集基金经理名称
        item['manager_description'] = response.xpath('/html/body/div[6]/div[2]/div[1]/div/div[1]/p/text()[2]').extract() #收集基金经理描述
        node_list = response.xpath('//td[@class="die"]|//td[@class="zhang"]')
        for node in node_list:
            revenue.append(node.xpath('./text()').extract())
        item['revenue'] = revenue
        item['accumulated_work_time'] = response.meta['accumulated_work_time']
        yield item


