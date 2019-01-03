# -*- coding: utf-8 -*-
import scrapy


class EplanningSpider(scrapy.Spider):
    name = 'eplanning'
    allowed_domains = ['eplanning.ie']
    start_urls = ['http://eplanning.ie/']


    def parse(self, response):
        urls=response.xpath('.//a/@href').extract()
        for url in urls:
        	if url=="#":
        		pass
        	else:
        		yield scrapy.Request(url,callback=self.parse_city)


    def parse_city(self,response):
    	app_url=response.xpath('.//*[@class="glyphicon glyphicon-inbox btn-lg"]/following-sibling::a/@href').extract_first()
    	yield scrapy.Request(response.urljoin(app_url),callback=self.parse_form)


    def parse_form(self,response):
    	yield scrapy.FormRequest.from_response(response,formdata={'RdoTimeLimit': '42'},formxpath='(//form)[2]',callback=self.parse_pages)


    def parse_pages(self,response):
    	application_url=response.xpath('//td/a/@href').extract()
    	for url in application_url:
    		yield scrapy.Request(response.urljoin(url),callback=self.parse_items)

    	nextpage_url=response.xpath('.//*[@rel="next"]/@href').extract_first()
    	yield scrapy.Request(response.urljoin(nextpage_url),callback=self.parse_pages)


    def parse_items(self,response):
    	agent_btn=response.xpath('.//*[@value="Agents"]/@style').extract_first()
    	if 'display: inline;  visibility: visible;' in agent_btn:
    		agent_name=response.xpath('//tr[th="Name :"]/td/text()').extract_first()
    		address_first=response.xpath('//tr[th="Address :"]/td/text()').extract_first()
    		address_second=response.xpath('//tr[th="Address :"]/following-sibling::tr/td/text()').extract()[0:3]
    		address_second=address_first+','.join(address_second)
    		phone=response.xpath('//tr[th="Phone :"]/td/text()').extract()
    		fax=response.xpath('//tr[th="Fax :"]/td/text()').extract()
    		email=response.xpath('//tr[th="e-mail :"]/td/text()').extract()
    		yield{	'agent name':agent_name,
					'address':address_second,
					'phone':phone,
					'fax':fax,
					'email':email,
					'URL':response.url}

    	else:
    		self.logger.info('Agent Button not Found or url does not exist')


