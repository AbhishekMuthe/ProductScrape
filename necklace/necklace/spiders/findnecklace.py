# -*- coding: utf-8 -*-
import scrapy

class FindnecklaceSpider(scrapy.Spider):
	name = 'findnecklace'
	allowed_domains = ['houseofindya.com']
	start_urls = ['http://houseofindya.com/']

	def parse(self, response):
		jewelry_link = response.xpath('.//nav/ul/li[17]/a/@href').extract_first()
		jewelry_link = response.urljoin(jewelry_link)
		yield scrapy.Request(url=jewelry_link, callback=self.necklace)
		
	def necklace(self, response):
		necklace_link = response.xpath('.//*[@class="seecatgTitle"][3]/a/@href').extract_first()
		necklace_set_link = response.xpath('.//*[@class="seecatgTitle"][4]/a/@href').extract_first()
		necklace_link = response.urljoin(necklace_link)
		necklace_set_link = response.urljoin(necklace_set_link)
		yield scrapy.Request(necklace_link, callback=self.product)
		yield scrapy.Request(necklace_set_link, callback=self.product)
		
		
	def product(self, response):
		products = response.xpath('.//ul/li/@data-url').extract()
		for product in products:
			product = ''.join(product)
			yield scrapy.Request(product, callback=self.product_details)
			
	def product_details(self, response):
		product_name = response.xpath('.//div[2]/h1/text()').extract_first()
		actual_price = response.xpath('//h4/span/text()').extract_first()
		discounted_price = response.xpath('//div/h4/span[2]/text()').extract_first()
		description =  response.xpath('//*[@id="tab-1"]/p/text()').extract_first()
		image_link = response.xpath('//ul/li/a/img/@data-original').extract_first()
		yield{'Product_Name': product_name,
				'Actual_Price': actual_price,
				'Discounted_Price': discounted_price,
			  'Description': description,
			  'img_link': image_link}