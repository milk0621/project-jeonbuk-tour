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

driver.get("https://www.google.co.kr/maps/")
time.sleep(2)

#검색창 찾기
search_box = driver.find_element(By.NAME, "q")
#전북특별자치도 부안군 변산면 새만금로 447-27 가력도항
#관광지이름 추출
df = pd.read_csv("./datas/region.csv")
review_data = []
titles = df["title"]
addrs = df["addr1"]
for title, addr in zip(titles, addrs):

    #검색어 입력 후 엔터
    search_box.clear()
    search_box.send_keys(addr+ title)
    search_box.send_keys(Keys.RETURN)

    time.sleep(2)

    sibling_count = None

    #검색결과가 두개 이상일때 첫번째 클릭
    try:
        search_result = driver.find_element(By.CSS_SELECTOR, "#QA0Szd > div > div > div.w6VYqd > div:nth-child(2) > div > div.e07Vkf.kA9KIf > div > div > div.m6QErb.DxyBCb.kA9KIf.dS8AEf.XiKgde.ecceSd > div.m6QErb.DxyBCb.kA9KIf.dS8AEf.XiKgde.ecceSd")

        #클래스가 없는 첫번째 div 선택
        search_result = search_result.find_element(By.XPATH, "./div[not(@class) or @class='']")
        
        siblings = search_result.find_elements(By.XPATH, "./preceding-sibling::div");
        #print(f"형제 개수: {len(siblings)}")

        sibling_count = len(siblings)

        #자식 선택 후 클릭
        search_result = search_result.find_element(By.CLASS_NAME, "hfpxzc")
        search_result.click()
    except Exception as e:
        print(e)
    
    #m6QErb DxyBCb kA9KIf dS8AEf XiKgde ecceSd
    #m6QErb DxyBCb kA9KIf dS8AEf XiKgde ecceSd

    #QA0Szd > div > div > div.w6VYqd > div.bJzME.tTVLSc > div > div.e07Vkf.kA9KIf > div > div > div.m6QErb.DxyBCb.kA9KIf.dS8AEf.XiKgde.ecceSd > div.m6QErb.DxyBCb.kA9KIf.dS8AEf.XiKgde.ecceSd

    #QA0Szd > div > div > div.w6VYqd > div.bJzME.tTVLSc > div > div.e07Vkf.kA9KIf > div > div > div.m6QErb.DxyBCb.kA9KIf.dS8AEf.XiKgde.ecceSd > div.m6QErb.DxyBCb.kA9KIf.dS8AEf.XiKgde.ecceSd
    time.sleep(2)
    try:
        review = driver.find_element(By.CSS_SELECTOR, ".hh2c6:nth-child(2)")
        review.click()
    except:
        continue

    time.sleep(2)

    score = driver.find_element(By.CSS_SELECTOR, ".fontDisplayLarge").text
    print(score)

    reviews = None

    total_reviews = driver.find_elements(By.CLASS_NAME, "jANrlb>div")[2].text
    total_reviews = int(re.sub(r"[^0-9\s]", "", total_reviews))
    time.sleep(2)
    
    try:
        if sibling_count != None:
            if sibling_count == 2:
                scroll_el = 'document.querySelector("#QA0Szd > div > div > div.w6VYqd > div.bJzME.Hu9e2e.tTVLSc > div > div.e07Vkf.kA9KIf > div > div > div.m6QErb.DxyBCb.kA9KIf.dS8AEf.XiKgde")'
            else:
                scroll_el = 'document.querySelector("#QA0Szd > div > div > div.w6VYqd > div:nth-child(2) > div > div.e07Vkf.kA9KIf > div > div > div.m6QErb.DxyBCb.kA9KIf.dS8AEf.XiKgde")'
        else :
            scroll_el = 'document.querySelector("#QA0Szd > div > div > div.w6VYqd > div:nth-child(2) > div > div.e07Vkf.kA9KIf > div > div > div.m6QErb.DxyBCb.kA9KIf.dS8AEf.XiKgde")'
    except:
        pass

    print(scroll_el)
        
    while True:
        print("while works!")
        reviews = driver.find_elements(By.CLASS_NAME, "jftiEf")
        height = driver.execute_script(f"return {scroll_el}.scrollHeight")
        driver.execute_script(f"{scroll_el}.scrollTo(0, {scroll_el}.scrollHeight)")
        time.sleep(2)
        new_heigth = driver.execute_script(f"return {scroll_el}.scrollHeight")
        if len(reviews) < 500:
            if total_reviews == len(reviews):
                break
        else:
            if len(reviews) >= 500:
                break
    #스크롤 전부 내린 후 출력
    for review in reviews:
        
        try:
            button_box = review.find_element(By.CLASS_NAME, "MyEned")
            if button_box and len(button_box.find_elements(By.TAG_NAME, "span")) >= 2:
                button = review.find_element(By.CLASS_NAME, "kyuRq")
                button.click()
            else:
                pass
        except:
            pass

        time.sleep(2)

        name = review.find_element(By.CLASS_NAME, "d4r55").text.strip()
        try:
            content = review.find_element(By.CLASS_NAME, "wiI7pd").text.strip()
        except:
            content = ""
        star = len(review.find_elements(By.CLASS_NAME, "elGi1d"))

        dict = {
            "관광지이름" : title,
            "총점" : score,
            "이름" : name,
            "내용" : content,
            "별점" : star
        }
        review_data.append(dict)
    
df = pd.DataFrame(review_data)
df.to_csv("review_data.csv", index=False, encoding="utf-8")

driver.quit()





