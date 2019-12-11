# -*- coding: utf-8 -*-
#!/usr/bin/python
import scrapy
from test_txt.items import TestTxtItem
from xml.etree import ElementTree
class QuotesSpider(scrapy.Spider):
    name = "link"
    start_urls = [
        'https://baosongngu.vn/category/world/'
    ]


    def create_xml():
        page = ElementTree.Element("Sentence")
        value = ElementTree.SubElement(page,"text")
        value.text = "value"
        value.set('id', '1')
        tree = ElementTree.ElementTree(page)
        tree.write("data.xml")
    create_xml()
    

    def parse(self, response):
        finalPage = response.xpath('//div[@class="theiaStickySidebar"]/div[@class="penci-pagination align-left"]/ul[@class="page-numbers"]/li/a/@href')[-2].extract()
        totalPage = int(finalPage.split("/")[-2])
        for page in range(totalPage):
            link = finalPage.replace(str(totalPage), str(page + 1))
            yield scrapy.Request(link, callback=self.crawlLink)

    def crawlLink(self, response):
        file = open('link.txt','a+')
        for link in response.xpath('//div[@class="theiaStickySidebar"]/ul[@class="penci-wrapper-data penci-grid"]/li/article/div/a/@href').extract():
            if link == 'https://baosongngu.vn/exercise-children-need/' : continue
            file.write(link + '\n')
            yield scrapy.Request(link, callback=self.saveFile)
    
    def saveFile(self, response):
        Raw = response.xpath('//div[@class="theiaStickySidebar"]/article/div/div[@class="inner-post-entry entry-content"]/p//text()').extract()

        def fix_Raw(list):
            string = ''
            for i in range(len(list)):
                string = string + ' ' + list[i]
            #Tach clgt
            string = string.split('Nguồn:')[0]
            string = string.split('New words:')[0]
            string = string.split('Người dịch:')[0]

            #Phan loai token
            token_spc1 = ['.”', '…”', '!', u'\xa0', '  ']  
            token_spc2 = ['”. ', '…”.','!. ', ' ', ' ']

            t_1 = ['U.S. ', 'Dr. ', 'sẻ.', 'Woolf chia sẻ,', 'nay, “Nó', '.” Ông' ]
            t_2 = ['U.S ', 'Dr.', 'sẻ:', 'Woolf chia sẻ.', 'nay. “Nó', '”, Ông' ]

            to_1 = ['(1)','(2)','(3)','(4)','(5)','(6)','(7)','(8)','(9)', '. 00']
            to_2 = ['','','','','','','','','', ',00']

            tok_1 = []
            tok_2 = []

            #Tach token
            token_in = t_1 + to_1 + tok_1 + token_spc1
            token_out = t_2 + to_2 + tok_2 + token_spc2
            for i in range(len(token_in)):
                string = string.replace(token_in[i],token_out[i]) 
            list_string = string.split('. ',)
            #Loai bo khoang trang
            while '' in list_string:
                list_string.remove('')            

            return list_string

        list_string = fix_Raw(Raw)

        #mo file xml 
        f = open('data.xml','a+')
        tree = ElementTree.parse('data.xml')
        root = tree.getroot()
        list_text = root.findall('text')
        n = len(list_text)
        num = int(list_text[n-1].get('id'))

        for i in range(len(list_string)):
            _text = ElementTree.Element('text')
            _text.set('id',str(num))
            num+=1
            _text.text = list_string[i] 
            root.append(_text)
        tree.write('data.xml')

        
    
