import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

class VovSpiderSpider(CrawlSpider):  
    name = "vov_spider"
    allowed_domains = ["vov.vn"]
    start_urls = ["https://vov.vn/"]

    rules = (
        Rule(
            LinkExtractor(allow_domains=["vov.vn"]), 
            callback="parse_item", 
            follow=True
        ),
    )


    def parse_item(self, response):  
        meta = dict()
        title = response.xpath('//h1/text()').get()
        date = response.xpath("//div[@class='col-md-4 mb-2']/text()").get().strip()
        
        meta["date"] = date
        meta["url"] = response.url

        paragraphs = response.xpath('//div[@class="row article-content"]//p/text()').getall()
        paragraphs = ["<start_of_turn> " + i + " <end_of_turn>" for i in paragraphs]

        yield {
            'title': title,  
            'content': paragraphs,
            'metadata': meta,
        }
