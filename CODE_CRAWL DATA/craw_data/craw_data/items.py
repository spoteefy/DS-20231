# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Job(scrapy.Item):
    # define the fields for your item here like:
    url = scrapy.Field()
    job = scrapy.Field()
    company = scrapy.Field()
    location = scrapy.Field()
    benefits = scrapy.Field()
    requirements = scrapy.Field()
    description = scrapy.Field()
    industry = scrapy.Field()
    level = scrapy.Field()
    skills = scrapy.Field()
    language = scrapy.Field()
    category = scrapy.Field()
    salary = scrapy.Field()
    working_time = scrapy.Field()
    experience = scrapy.Field()
    number = scrapy.Field()
