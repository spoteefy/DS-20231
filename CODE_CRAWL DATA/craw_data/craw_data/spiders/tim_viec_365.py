
from datetime import datetime, timedelta, tzinfo

import scrapy

from craw_data.items import Job



# Tạo lớp con của tzinfo để cung cấp thông tin về múi giờ
class CustomTimezone(tzinfo):
    def __init__(self, offset):
        self.offset = offset

    def utcoffset(self, dt):
        return self.offset

    def dst(self, dt):
        return timedelta(0)


# Tạo đối tượng tzinfo tùy chỉnh
custom_tz = CustomTimezone(timedelta(hours=7))


class TimViec365Spider(scrapy.spiders.SitemapSpider):
    name = "tim_viec_365"
    allowed_domains = ['timviec365.vn']
    sitemap_urls = ['https://timviec365.vn/sitemap.xml']
    sitemap_follow = [r'sitemap-job\d+\.xml']


    def sitemap_filter(self, entries):
        for entry in entries:
            date_time = datetime.strptime(entry["lastmod"], "%Y-%m-%dT%H:%M:%S%z")
            if date_time >= datetime(2023, 9, 23, 0, 0, 29, 0, custom_tz):
                yield entry

    def parse(self, response):
        job = Job()
        job['url'] = response.url
        job['job'] = response.xpath('*//div[@class="com_info"]//h1[@class="com_post"]/text()').get()
        job['company'] = response.xpath(
            '*//div[@class="com_info"]//a[@class="com_name"]//p[@class="com_name_text"]/text()').get()
        job['location'] = response.xpath('*//p[contains(text(), "Địa điểm làm việc")]/following-sibling::div[1]//p[contains(text(), "Tỉnh thành")]/following-sibling::*[1]/text()').get()
        job['benefits'] = response.xpath('*//div[h2[contains(text(), "QUYỀN LỢI")]]/following-sibling::div[1]/text()').getall()
        job['requirements'] = response.xpath('//div[contains(@class, "text_content") and contains(@class, "ycau_tdung")]/text()').getall()
        job['description'] = response.xpath('//h2[contains(text(), "MÔ TẢ CÔNG VIỆC")]/../following-sibling::div[1]/text()').getall()
        job['industry'] = response.xpath('//p[contains(text(), "Lĩnh vực")]/a/text()').get()
        job['category'] = response.xpath('*//p[contains(text(),"Ngành nghề:")]/a/text()').getall()
        job['level'] = None
        job['language'] = None
        job['skills'] = []
        job['salary'] = response.xpath('*//p[contains(text(), "Mức lương")]/span/text()').get()
        job['working_time'] = response.xpath('*//p[contains(text(), "Hình thức làm việc")]/following-sibling::*[1]/text()').get()
        job['experience'] = response.xpath('*//p[@class="item_if" and contains(text(), "Kinh nghiệm")]/following-sibling::*[1]/text()').get()
        job['number'] = response.xpath('*//p[@class="item_if" and contains(text(), "Số lượng cần tuyển")]/following-sibling::*[1]/text()').get()
        yield job

