import os
import json
import time
from tqdm import tqdm

import selenium.common.exceptions as exceptions
import undetected_chromedriver as uc

from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


def get_detail(driver, url):
    driver.get(url)
    driver.implicitly_wait(5)
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#main"))
        )
    except:
        print(url)
        return {}
    web_type = 0  # 0 is common web, 1 is brand viettel like web, 2 is brand fptedu like web
    if url.startswith("https://www.topcv.vn/brand/"):
        try:
            driver.find_element(By.CSS_SELECTOR, "h2.title")
            web_type = 2
        except:
            web_type = 1

    try:
        if web_type == 0:
            company = driver.find_element(By.CSS_SELECTOR, 'h2.company-name-label a').get_attribute('innerText')
            general_info = driver.find_elements(By.CSS_SELECTOR, ".box-general-group-info-value")
            general_info = [gi.get_attribute("innerText") for gi in general_info]
            categories = driver.find_element(By.CSS_SELECTOR, ".box-category-tags").find_elements(By.XPATH, '*')
            categories = [category.get_attribute("innerText") for category in categories]
            details = driver.find_elements(By.CSS_SELECTOR, ".job-description__item--content")
            details = [d.get_attribute("innerText") for d in details[:4]]
            time.sleep(10)
            return {
                "company": company,
                "description": details[0],
                "requirements": details[1],
                "benefits": details[2],
                "location": details[3],
                "category": categories,
                "level": general_info[0],
                "working_time": general_info[3]
            }

        elif web_type == 1:
            company = driver.find_element(By.CSS_SELECTOR, 'h1.company-content__title--name').get_attribute('innerText')
            details = driver.find_elements(By.CSS_SELECTOR, ".premium-job-description__box--content")
            details = [detail.get_attribute("innerText") for detail in details]
            general_info = driver.find_elements(By.CSS_SELECTOR, ".general-information-data__value")
            general_info = [gi.get_attribute("innerText") for gi in general_info]
            categories = driver.find_elements(By.CSS_SELECTOR, ".tag-item")
            categories = [category.get_attribute("innerText") for category in categories]
            time.sleep(10)

            return {
                "company": company,
                "description": details[0],
                "requirements": details[1],
                "benefits": details[2],
                "category": categories,
                "level": general_info[0],
                "working_time": general_info[2]
            }
        else:
            company = driver.find_element(By.CSS_SELECTOR, '.footer-info-company-name').get_attribute('innerText')
            info = driver.find_elements(By.CSS_SELECTOR, ".box-info")
            general_info = info[0].find_elements(By.CSS_SELECTOR, ".box-item span")[:6]
            general_info = [gi.get_attribute("innerText") for gi in general_info]
            details = [i.find_element(By.CSS_SELECTOR, ".content-tab").get_attribute("innerText") for i in info[1:4]]
            location = driver.find_element(By.CSS_SELECTOR, ".box-address > div").get_attribute("innerText")
            categories = driver.find_elements(By.CSS_SELECTOR, ".item > a")
            categories = [category.get_attribute("innerText") for category in categories]
            time.sleep(10)
            return {
                "company": company,
                "description": details[0],
                "requirements": details[1],
                "benefits": details[2],
                "location": location,
                "category": categories,
                "level": general_info[3],
                "working_time": general_info[2]
            }
    except exceptions.NoSuchElementException as e:
        print(e.msg)
        print(web_type, url)
        return {}
    except:
        print(web_type, url)
        return {}


options = uc.ChromeOptions()
options.headless = False  # Set headless to False to run in non-headless mode
driver = uc.Chrome(use_subprocess=True, options=options)
# driver = webdriver.Chrome()

# # url = "https://www.topcv.vn/brand/congnghiepvienthongquandoi/tuyen-dung/backend-developer-luong-tu-15-35-trieu-j1155667.html?ta_source=JobSearchList_LinkDetail"
# url = "https://www.topcv.vn/viec-lam/senior-flutter-engineer-upto-60-m/1140364.html?ta_source=JobSearchList_LinkDetail"
# # url = "https://www.topcv.vn/brand/tek-experts/tuyen-dung/it-support-ho-tro-ky-thuat-j750310.html?ta_source=JobSearchList_LinkDetail"
# print(get_detail(driver, url))

for i in range(100, 101):
    with open(f"v0/jobs-{i}.json", 'r', encoding='utf8') as f:
        items = json.load(f)

    for item in tqdm(items):
        # if item.get('company', '') == '' or item.get('location', '') == '':
        detail = get_detail(driver, item['url'])
        item.update(detail)

    with open(f"v2/jobs-{i}.json", "w", encoding="utf8") as f:
        json.dump(items, f, indent=2, ensure_ascii=False)

# print(get_detail(driver, "https://www.topcv.vn/viec-lam/ke-toan-chi-phi/1163796.html?ta_source=JobSearchList_LinkDetail&u_sr_id=jMrER7kogjwXZP9k3zhRJ904YxwtuA8nYRPJGtn0_1699548197"))
driver.quit()
