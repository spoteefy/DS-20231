import random
from urllib.parse import urlparse, urlunparse, parse_qs
import scrapy
import re
from scrapy.http import Request
from dev_cr_ds.items import JobScraperItem

def clean_query_parameters(self, url):
    parsed_url = urlparse(url)
    query_parameters = parse_qs(parsed_url.query)
    # Loại bỏ các tham số
    query_parameters.pop('job_selected', None)
    query_parameters.pop('lab_feature', None)
    query_parameters.pop('click_source', None)
    query_parameters.pop('source', None)
    query_parameters.pop('locale', None)

    clean_url = urlunparse((
        parsed_url.scheme, parsed_url.netloc, parsed_url.path, parsed_url.params, '', ''
    ))
    if query_parameters:
        clean_url += '?' + '&'.join(f'{key}={value[0]}' for key, value in query_parameters.items())
    return clean_url
    
class ItviecSpider(scrapy.Spider):
    name = 'itviec'
    allowed_domains = ['itviec.com']
    start_urls = ['https://itviec.com/viec-lam-it/data-scientist-python-sql-aws-credit360-ai-1313']
    login_url = 'https://itviec.com/dang-nhap-tai-khoan'

    def start_requests(self):
        yield scrapy.Request(self.login_url, callback=self.parse)

    def parse(self, response):
        token = response.xpath('/html/head/meta[10]/@content').get()
        print(token)
        # create form value
        data = {
            'authenticity_token': token,
            'user[email]': 'v.thng028@gmail.com',
            'user[password]': 'Tho.NV204694',
            'locale': 'vi'
        }
        # Submit Post request login
        yield scrapy.FormRequest(url=self.login_url, formdata=data, callback=self.after_login)
    
    def after_login(self, response):
        check_login = response.xpath('/html/body/header/nav/div/div[2]/ul[2]/li[2]/div[2]/ul/li[2]/a/span/text()').get()
        print(check_login)
        if check_login == "Việc làm của tôi":
            print("Login successful")
            for url in self.start_urls:
                yield scrapy.Request(url, callback=self.parse_job_page)
        else:
            print("FAIL")

    def parse_job_page(self, response):

        # Sử dụng XPath để trích xuất trường
        title = response.xpath('/html/body/main/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/h1/text()').get()
        address = response.xpath('/html/body/main/div[1]/div[2]/div[1]/div[1]/div[2]/div/div/div[1]/span/text()').get()
        salary = response.xpath('/html/body/main/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[2]/div//text()').getall()
        print(salary)
        i = 2
        job_type = response.xpath(f'/html/body/main/div[1]/div[2]/div[1]/div[1]/div[2]/div/div/div[{i}]/div/span/text()').get()
        if not job_type:
            i = i + 1
            job_type = response.xpath(f'/html/body/main/div[1]/div[2]/div[1]/div[1]/div[2]/div/div/div[{i}]/div/span/text()').get()
        if not job_type:
            i = i + 1
            job_type = response.xpath(f'/html/body/main/div[1]/div[2]/div[1]/div[1]/div[2]/div/div/div[{i}]/div/span/text()').get()

        company = response.xpath('/html/body/main/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/text()').get()

        i = i + 1
        skills = response.xpath(f'/html/body/main/div[1]/div[2]/div[1]/div[1]/div[2]/div/div/div[{i}]/a/div/text()').getall()
        if not skills:
            i = i + 1
            skills = response.xpath(f'/html/body/main/div[1]/div[2]/div[1]/div[1]/div[2]/div/div/div[{i}]/a/div/text()').getall()
            
        skills = [re.sub(r'[^\w\s,.!?&$:-_;/]', '', skill) for skill in skills]
        skills = [skill.strip() for skill in skills]

        i = 1

        reasons = response.xpath(f'/html/body/main/div[1]/div[2]/div[1]/div[1]/section/div[{i}]//text()[not(ancestor::h2)]').getall()
        check_r = response.xpath(f'/html/body/main/div[1]/div[2]/div[1]/div[1]/section/div[{i}]/h2/text()').get()
        if check_r == "3 Lý do để gia nhập công ty":
            reasons = [re.sub(r'[^\w\s,.!?&$:-_;/]', '', reason) for reason in reasons]
            reasons = [reason.strip() for reason in reasons]
        else:
            reasons = []
            i = i - 2

        i = i + 2
        description = response.xpath(f'/html/body/main/div[1]/div[2]/div[1]/div[1]/section/div[{i}]//text()[not(ancestor::h2)]').getall()
        check_d = response.xpath(f'/html/body/main/div[1]/div[2]/div[1]/div[1]/section/div[{i}]/h2/text()').get()
        if check_d == "Mô tả công việc":
            description = [re.sub(r'[^\w\s,.!?&$:-_;/]', '', des) for des in description]
            description = [de.strip() for de in description]
        else:
            description = []
            i = i - 2

        i = i + 2
        requirement = response.xpath(f'/html/body/main/div[1]/div[2]/div[1]/div[1]/section/div[{i}]//text()[not(ancestor::h2)]').getall()
        check_re = response.xpath(f'/html/body/main/div[1]/div[2]/div[1]/div[1]/section/div[{i}]/h2/text()').get()
        if check_re == "Yêu cầu công việc":
            requirement = [re.sub(r'[^\w\s,.!?&$:-_;/]', '', req) for req in requirement]
            requirement = [req.strip() for req in requirement]
        else:
            requirement = []
            i = i - 2
        
        i = i + 2
        benefits_work = response.xpath(f'/html/body/main/div[1]/div[2]/div[1]/div[1]/section/div[{i}]//text()[not(ancestor::h2)]').getall()
        check_b = response.xpath(f'/html/body/main/div[1]/div[2]/div[1]/div[1]/section/div[{i}]/h2/text()').get()
        if check_b == "Tại sao bạn sẽ yêu thích làm việc tại đây":
            benefits_work = [re.sub(r'[^\w\s,.!?&$:-_;/]', '', bene) for bene in benefits_work]
            benefits_work = [bene.strip() for bene in benefits_work]
        else:
            benefits_work = []
            i = i - 2

        if title:
            item = JobScraperItem()
            item['url'] = response.url
            item['title'] = title
            item['salary'] = salary
            item['company'] = company.strip()
            item['address'] = address
            item['job_type'] = job_type
            item['skills'] = skills
            item['reason'] = ' '.join(reasons)
            item['description'] =  ' '.join(description)
            item['requirement'] = ' '.join(requirement)
            item['benefits_work'] = ' '.join(benefits_work)
            yield item

        # Trích xuất và follow tất cả các liên kết có tiền tố mong muốn
        links = response.css('a::attr(href)').extract()
        for link in links:
            link = clean_query_parameters(self, link)
    
            if not link.startswith('https://'):
                link = 'https://itviec.com' + link

            if link.startswith('https://itviec.com/viec-lam-it'):
                yield scrapy.Request(link, callback=self.parse_job_page)