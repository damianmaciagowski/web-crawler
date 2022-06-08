import scrapy
from scrapy.loader import ItemLoader
from webcrawler.items import KomputronikItem


class KomputronikSpider(scrapy.Spider):
    name = "komputronik"
    allowed_domains = ["komputronik.pl"]

    def start_requests(self):
        urls = [
            "https://www.komputronik.pl/search-filter/5801/komputery-do-gier",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        computer_hrefs = response.xpath(
            "//ul[@class='product-entry2-wrap']/li/div/div[1]/a/@href"
        ).extract()

        yield from response.follow_all(computer_hrefs, self.parsejobpage)

    def parsejobpage(self, response):
        item_loader = ItemLoader(item=KomputronikItem(), selector=response)
        item_loader.add_xpath(
            "computer_name",
            "//div[@class='pgrid-container']//div[@id='p-inner-left']//section//h1//text()",
        )
        item_loader.add_xpath(
            "price", "//div[@id='p-inner']/div[2]//span[@class='price']/span[1]/text()"
        )
        item_loader.add_xpath(
            "producer",
            "//div[@class='full-specification']/div[1]/table/tbody/tr[1]/td/a/text()",
        )
        item_loader.add_xpath(
            "processor_type",
            "//div[@class='full-specification']//div[2]//table//tbody//tr[1]//td//a//text()",
        )
        yield item_loader.load_item()
