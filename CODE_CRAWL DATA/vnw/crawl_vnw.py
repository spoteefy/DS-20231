import argparse
from selenium import webdriver
import concurrent.futures
import time
import threading
from bs4 import BeautifulSoup
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from tqdm import tqdm

ROOT_URL = 'https://www.vietnamworks.com'

def write_row(file, row):
    with open(file, 'a', encoding='utf8') as f:
        f.write(row + '\n')

def get_drive():
    options = Options()

    options.add_argument('--headless')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')

    # service = Service(executable_path=r'/usr/bin/chromedriver')
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(options=options, service=service)

    return driver

def crawl_url(driver, url, output_file):
    driver.get(url)
    
    time.sleep(1)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
    
    html_content = driver.page_source
    soup = BeautifulSoup(html_content, 'html.parser')
    
    elements = soup.select('div.sc-ikHNZD.loEdRV a')
    elements = [ROOT_URL+element['href'] for element in elements]
    
    if len(elements) != 50:
        with open("error.txt", "a") as f:
            f.write(url + '\n')
    else:
        write_row(output_file, '\n'.join(elements))

if __name__ == '__main__':
    driver = get_drive()

    parser = argparse.ArgumentParser()
    parser.add_argument('--start_page', type=int, default=1)
    parser.add_argument('--last_page', type=int, default=178)
    parser.add_argument('--output_file', type=str, default='job_urls.txt')
    args = parser.parse_args()

    urls = [f'https://www.vietnamworks.com/viec-lam?page={i}' for i in range(args.start_page, args.last_page + 1)]
    for i, url in tqdm(enumerate(urls)):
        crawl_url(driver, url, args.output_file)

    driver.quit()