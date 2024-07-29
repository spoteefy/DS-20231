from bs4 import BeautifulSoup

from test import get_drive

import json
import time

from tqdm import tqdm
def extract_data(html_content, url):
    data = {}
    soup = BeautifulSoup(html_content, 'html.parser')
    # url
    data['url'] = url
    # job
    title = soup.select_one('h1.job-title').find(text=True, recursive=False).strip()
    data['job'] = title
    # company
    company_name = soup.select_one('div.company-name span.name')
    data['company'] = company_name.text.strip()
    # location
    location = soup.select_one('div.location-name')
    data['location'] = location.text.strip()
    # benefits
    benefits = soup.select('div.benefit-name')
    data['benefits'] = [benefit.text.strip() for benefit in benefits]    # requirements
    # requirements
    requirements = soup.select_one('div.requirements')
    data['requirements'] = requirements.text.strip()
    # description
    job_description = soup.select_one('div.job-description div.description')
    data['description'] = job_description.text.strip()
    summary_elems = soup.select('div.row.summary-item')
    summary_data = {}
    for elem in summary_elems:
        k = elem.select_one('span.content-label')
        v = elem.select_one('span.content')
        if k and v:
            summary_data[k.text.strip()] = v.text.strip()
    # summary_data = {elem.select_one('span.content-label').text.strip(): elem.select_one('span.content').text.strip() for elem in summary_elems}
    # industry
    data['industry'] = summary_data.get('Ngành Nghề', "")
    # category
    data['category'] = summary_data.get('Lĩnh vực', "")
    # skills
    data['skills'] = summary_data.get('Kỹ Năng', "")
    # level
    data['level'] = summary_data.get('Cấp Bậc', "")
    # language
    data['language'] = summary_data.get('Ngôn Ngữ Trình Bày Hồ Sơ', "")
    # salary
    salary = soup.select_one('span.salary')
    data['salary'] = salary.text.strip()
    # # working_time
    # data['working_time'] = ""
    # # experience
    # data['experience'] = ""
    
    return data

if __name__ == '__main__':
    driver = get_drive()
    with open("job_urls.txt", "r") as f:
        urls = f.read().split('\n')
    
    for url in tqdm(urls):
        try:
            driver.get(url)
            time.sleep(2)
            
            html_content = driver.page_source
            data = extract_data(html_content, url)
            
            with open("data.jsonl", "a", encoding="utf-8") as file:
                json_str = json.dumps(data, ensure_ascii=False)
                file.write(json_str + "\n")
        except:
            with open("error.txt", "a") as f:
                f.write(url + '\n')
x
