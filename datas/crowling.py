import pandas as pd
import subprocess
import time
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

#관광지이름 추출
df = pd.read_csv("./datas/region.csv")
title = df["title"]

#봇우회 코드
chrome_browser = subprocess.Popen(r'C:\Program Files\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\chromeCookie"')

options = Options()
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36")
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--ignore-certificate-errors')
options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

driver.get("https://www.google.co.kr/maps/")
time.sleep(2)

#검색창 찾기
search_box = driver.find_element(By.NAME, "q")

#검색어 입력 후 엔터
search_box.send_keys("전주 한옥마을")
search_box.send_keys(Keys.RETURN)

time.sleep(2)

review = driver.find_element(By.CSS_SELECTOR, ".hh2c6:nth-child(2)")
review.click()

score = driver.find_element(By.CLASS_NAME, "fontDisplayLarge").text

time.sleep(2)

reviews = None

total_reviews = driver.find_elements(By.CLASS_NAME, "jANrlb>div")[2].text
total_reviews = int(re.sub(r"[^0-9\s]", "", total_reviews))

time.sleep(2)

scroll = driver.find_element(By.CSS_SELECTOR, "#QA0Szd > div > div > div.w6VYqd > div:nth-child(2) > div > div.e07Vkf.kA9KIf > div > div > div.m6QErb.DxyBCb.kA9KIf.dS8AEf.XiKgde")
print(total_reviews, type(total_reviews))
print(scroll.get_attribute('innerHTML'))

scroll_el = 'document.querySelector("#QA0Szd > div > div > div.w6VYqd > div:nth-child(2) > div > div.e07Vkf.kA9KIf > div > div > div.m6QErb.DxyBCb.kA9KIf.dS8AEf.XiKgde")'

while True:
    reviews = driver.find_elements(By.CLASS_NAME, "jftiEf")
    
    height = driver.execute_script(f"return {scroll_el}.scrollHeight")
    driver.execute_script(f"{scroll_el}.scrollTo(0, {scroll_el}.scrollHeight)")
    time.sleep(2)
    new_heigth = driver.execute_script(f"return {scroll_el}.scrollHeight")
    if len(reviews) < 10:
        if total_reviews == reviews:
            break
    else:
        if len(reviews) >= 10:
            break
    
print(len(reviews))

#스크롤 전부 내린 후 출력

review_data = []

for review in reviews:
    name = review.find_element(By.CLASS_NAME, "d4r55").text.strip()
    
    
    dict = {
        "이름" : name
    }
    review_data.append(dict)
    
df = pd.DataFrame(review_data)
# df.to_csv("review_data.csv", index=False, encoding="utf-8")
print(df)


driver.quit()





