# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import unicodedata
import scrapy
from itemloaders.processors import TakeFirst, MapCompose, Compose
from w3lib.html import remove_tags, strip_html5_whitespace


class KomputronikItem(scrapy.Item):
    computer_name = scrapy.Field(
        input_processor=MapCompose(remove_tags, strip_html5_whitespace),
        output_processor=TakeFirst(),
    )
    price = scrapy.Field(
        input_processor=MapCompose(remove_tags, strip_html5_whitespace),
        output_processor=Compose(
            lambda v: unicodedata.normalize("NFKD", v[0])
            .strip()
            .replace(" ", "")
        ),
    )
    producer = scrapy.Field(
        input_processor=MapCompose(remove_tags, strip_html5_whitespace),
        output_processor=Compose(lambda v: v[1]),
    )
    processor_type = scrapy.Field(
        input_processor=MapCompose(remove_tags, strip_html5_whitespace),
        output_processor=Compose(lambda v: v[1]),
    )
