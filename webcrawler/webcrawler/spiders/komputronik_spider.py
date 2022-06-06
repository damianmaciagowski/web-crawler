import scrapy
import unicodedata

class KomputronikItem(scrapy.Item):
    computer_name = scrapy.Field()
    price = scrapy.Field()
    producer = scrapy.Field()
    processor_type = scrapy.Field()

class KomputronikSpider(scrapy.Spider):
    name = "komputronik"
    allowed_domains = ['komputronik.pl'] 
    stripped_computer_names = []
    def start_requests(self):
        urls = [
            'https://www.komputronik.pl/search-filter/5801/komputery-do-gier',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        item = KomputronikItem()
        computer_names = response.xpath("//ul[@class='product-entry2-wrap']/li/div/div[1]/a/text()").extract()
        stripped_computer_names = [s.strip() for s in computer_names]
        computer_hrefs = response.xpath("//ul[@class='product-entry2-wrap']/li/div/div[1]/a/@href").extract()
        x = 0
        for product_page in computer_hrefs:
            item["computer_name"] = stripped_computer_names[x]
            x += 1
            yield scrapy.Request(url=product_page, callback=self.parsejobpage, meta=item)
    def parsejobpage(self, response):
        item = KomputronikItem()
        d = {}
        price = response.xpath("//div[@id='p-inner']/div[2]//span[@class='price']/span[1]/text()").extract()
        producer = response.xpath("//div[@class='full-specification']/div[1]/table/tbody/tr[1]/td/a/text()").extract()
        processor_type = response.xpath("//div[@class='full-specification']/div[2]/table/tbody/tr[1]/td/a/text()").extract()
        price_stripped = unicodedata.normalize("NFKD", price[0]).strip().replace(" ", "")
        item["computer_name"] = response.meta.get("computer_name")
        item["price"] = price_stripped
        item["producer"] = producer[1].strip()
        item["processor_type"] = processor_type[0].strip()
        yield item
