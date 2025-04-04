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

#봇우회 코드
chrome_browser = subprocess.Popen(r'C:\Program Files\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\chromeCookie"')

options = Options()
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36")
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--ignore-certificate-errors')
options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

driver.get("https://map.naver.com/")
time.sleep(2)

#검색창 찾기
search_box = driver.find_element(By.ID, "#input_search1743732776208")

df = pd.read_csv("./datas/region.csv")
review_data = []
titles = df["title"]
# titles = ["전북 전주 한옥마을"]
addrs = df["addr1"]
# addrs = ["전북특별자치도 전주시 완산구 기린대로 99"]

"""
    1. 주소 + 이름 검색하면 결과가 주소만나오고, 관광지정보가 안나오는경우
     -> 이름만 검색하면 나오긴함

    2. 
"""

for title, addr in zip(titles, addrs):
    #검색어 입력 후 엔터
    search_box.clear()
    search_box.send_keys(addr+ title)
    search_box.send_keys(Keys.RETURN)
    
    time.sleep(2)
    continue
    # try:
    #     search_result = driver.find_elements(By.CSS_SELECTOR, "#_pcmap_list_scroll_container > ul > li")
        
    #     el = len(search_result)
    #     print(el)
        
    #     if el > 0:
    #         #검색결과 여러개
    #         print("검색결과 여러개")
    #         key = search_result[0].find_element(By.CLASS_NAME, "qbGlu")
    #         key.click()
    #     else:
    #         #검색결과 한개 or 없을때
    #         print("검색결과 한개 or 없음")
    # except:
    #     print("x")
    
    
    
    # dict = {
    #     "관광지이름" : title,
    #     "총점" : "score",
    #     "이름" : "name",
    #     "내용" : "conten"
    # }