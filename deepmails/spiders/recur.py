# -*- coding: utf-8 -*-
from scrapy.spiders import CrawlSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
from scrapy.utils.markup import remove_tags
import re,sys,urlparse
reload(sys)
sys.setdefaultencoding('utf8')
ban_chars = ["callto","mail","javascript","facebook","twitter","plus.google"]
default_link = "http://www.nordcert.se/"
crawledLinks= []

class DeepSpider(CrawlSpider):
    name= "recurcrawl"
    # allowed_domains    = ["net.tutsplus.com"]
    rotate_user_agent = True
    start_urls =["http://www.nordcert.se/sv/kontakt-nordcert/"]

    def parse(self, response):
        # hxs= HtmlXPathSelector(response)
        # links= hxs.xpath("//a/@href").extract()
        links = response.xpath("//a/@href").extract()
        # # linkz = response.xpath("//div[@class='columned-project-list']/div/ul/li/a/@href").extract()
        # #We stored already crawled links in this list
        # # print linkz
        # #Pattern to check proper link
        # # linkPattern     = re.compile("^(?:ftp|http|https):\/\/(?:[\w\.\-\+]+:{0,1}[\w\.\-\+]*@)?(?:[a-z0-9\-\.]+)(?::[0-9]+)?(?:\/|\/(?:[\w#!:\.\?\+=&amp;%@!\-\/\(\)]+)|\?(?:[\w#!:\.\?\+=&amp;%@!\-\/\(\)]+))?$")
        for link in links:
        # # # If it is a proper link and is not checked yet, yield it to the Spider
            if not link in crawledLinks and not any(each in link for each in ban_chars):
                crawledLinks.append(link)
                final_link = urlparse.urljoin(default_link,link.replace("../",""))
                if default_link in final_link :    
                    yield Request(final_link,self.parse)
        body = response.xpath("//body").extract()
        # emails_raw = response.xpath("//div[@class='content-text']/table/tbody/tr/td/p/a").extract()
        # print body
        # for each in emails_raw:
            # print remove_tags(each)
        emails =re.findall(r'[\w\-][\w\-\.]+@[\w\-][\w\-\.]+[a-zA-Z]{1,4}',str(body).replace("<!--y-->","").replace("<!--x-->","").replace("<br></br>",""))
        # emails =re.findall(r'[\w\-][\w\-\.]+\(at\)[\w\-][\w\-\.]+[a-zA-Z]{1,4}',str(body).replace("<!--y-->","").replace("<!--x-->","").replace("<br></br>",""))##(at)use huda
        # print emails
        with open("crawlables.txt","a") as writeemail:
            if emails:
                writeemail.write("\n".join(emails)+"\n")
        # titles    = hxs.select('//h1[@class="post_title"]/a/@href').extract()
        # for title in titles:
        #     item= NettutsItem()
        #     item["title"]     = title
        #     yield item

    # # def parse_mail(self,response):
