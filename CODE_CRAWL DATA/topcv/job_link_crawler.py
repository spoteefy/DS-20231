import os
import json
import time

import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys


def get_job(driver, base_url, page):
    driver.get(base_url + str(page))
    try:
        items = WebDriverWait(driver, 60).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.body"))
        )
    except:
        print(page)
        error_pages.append(str(page))
        return []

    detail = []
    for item in items:
        try:
            name_section = item.find_element(By.CSS_SELECTOR, 'h3.title > a')
            url = name_section.get_attribute('href')
            job = name_section.get_attribute('text')
            salary = item.find_element(By.CSS_SELECTOR, 'label.title-salary').get_attribute("innerText")
            company = item.find_element(By.CSS_SELECTOR, 'a.company').get_attribute("innerText")
            location = item.find_element(By.CSS_SELECTOR, 'label.address').get_attribute("innerText")
            detail.append({
                "url": url,
                "job": job,
                "company": company,
                "location": location,
                "salary": salary
            })
        except:
            detail.append({})
    time.sleep(10)
    return detail


base_url = "https://www.topcv.vn/tim-viec-lam-moi-nhat?sort=new&page="

options = uc.ChromeOptions()
options.headless = False  # Set headless to False to run in non-headless mode
driver = uc.Chrome(use_subprocess=True, options=options)
# driver = webdriver.Chrome()

for patch in range(100):
    details = []
    error_pages = []
    for i in range(4):
        detail = get_job(driver, base_url, page=patch*4 + i + 1)
        details += detail
    with open(f"v0/jobs-{patch}.json", "w", encoding='utf8') as f:
        json.dump(details, f, indent=2, ensure_ascii=False)
    if len(error_pages) == 0: continue
    with open(f"v0/error_pages.txt", 'a') as f:
        f.write(" ".join(error_pages) + " ")

## run this block after above block
# with open(f"v0/error_pages.txt", 'r') as f:
#     pages = f.read().split()
# details = []
# error_pages = []
# for page in pages:
#     detail = get_job(driver, base_url, page)
#     details += detail
# with open("v0/jobs-100.json", 'w', encoding='utf8') as f:
#     json.dump(details, f, indent=2, ensure_ascii=False)

driver.quit()
