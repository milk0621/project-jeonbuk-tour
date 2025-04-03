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
df = pd.read_csv("./datas/pre_region_data.csv")
review_data = []
titles = ["가력도항", "갑오 동학혁명 100주년 기념탑", "객사길", "광제정", "고창갯벌 (전북 서해안 국가지질공원)"]
#titles = ["고창갯벌 (전북 서해안 국가지질공원)"]

addrs = ["전북특별자치도 부안군 변산면 새만금로 447-27", "전북특별자치도 정읍시 내장호반로 214", "전북특별자치도 전주시 완산구 중앙동2가 10-1", "전북특별자치도 임실군 삼계면 세심길 82", "전북특별자치도 고창군 심원면 만돌리"]
#addrs = ["전북특별자치도 고창군 심원면 만돌리"]

#케이스
#1. 결과 여러개
#1-1. 검색결과 텍스트 표출 -> 클릭하면 서브메뉴에 스크롤 -> 객사길
#1-2. 부분일치 텍스트 표출 -> 클릭하면 메인메뉴에 스크롤 -> 가력도항
#1-3. 텍스트 표출 없음 -> 클릭하면 서브메뉴에 스크롤 ->고창갯벌 (전북 서해안 국가지질공원)

#2. 결과 한개
#2-1. 리뷰버튼 있음 -> 클릭하면 메인메뉴에 스크롤 -> 갑오 동학혁명 100주년 기념탑
#2-2. 리뷰버튼 없음 -> 건너뛰기 -> 광제정

#3. 


for title, addr in zip(titles, addrs):

    #검색어 입력 후 엔터
    search_box.clear()
    search_box.send_keys(addr+ title)
    search_box.send_keys(Keys.RETURN)

    time.sleep(2)

    el = None
    sibling_count = None
    #검색결과가 두개 이상일때 첫번째 클릭
    # #QA0Szd > div > div > div.w6VYqd > div:nth-child(2) > div > div.e07Vkf.kA9KIf > div > div > div.m6QErb.DxyBCb.kA9KIf.dS8AEf.XiKgde.ecceSd > div.m6QErb.DxyBCb.kA9KIf.dS8AEf.XiKgde.ecceSd
    try:
        search_result = driver.find_elements(By.CSS_SELECTOR, "#QA0Szd > div > div > div.w6VYqd > div:nth-child(2) > div > div.e07Vkf.kA9KIf > div > div > div.m6QErb.DxyBCb.kA9KIf.dS8AEf.XiKgde.ecceSd > div.m6QErb.DxyBCb.kA9KIf.dS8AEf.XiKgde.ecceSd")
        
        el = len(search_result)
        print(el)
        if el > 0:
            #검색결과 여러개
            key = search_result[0].find_elements(By.XPATH, "./preceding-sibling::div")
            #print("검색결과 이전형제",len(key))
            el_child = len(key)
            print(el_child)
            #부분일치 일 때 이전형제 개수 : 1
            #검색결과 나올 때 이전형제 개수 : 0
            #텍스트 없을 때 이전형제 개수 : 0
            if el_child > 0:
                #부분일치(메인메뉴 스크롤)
                print("부분일치")
                main_menu = search_result[0].find_elements(By.XPATH, "./div[not(@class) or @class='']")
                if "스폰서" in main_menu[0].get_attribute("innerText"):
                    main_menu[1].click()
                else:
                    main_menu[0].click()
                
                #리뷰클릭
                time.sleep(2)
                review_btn = driver.find_element(By.CSS_SELECTOR, "#QA0Szd > div > div > div.w6VYqd > div:nth-child(2) > div > div.e07Vkf.kA9KIf > div > div > div:nth-child(3) > div > div > button:nth-child(2)")
                review_btn.click()

                scroll_el = 'document.querySelector("#QA0Szd > div > div > div.w6VYqd > div:nth-child(2) > div > div.e07Vkf.kA9KIf > div > div > div.m6QErb.DxyBCb.kA9KIf.dS8AEf.XiKgde")'
                
                #메인메뉴 스크롤
            else :
                print("검색결과 or no 텍스트")
                #검색결과 or 텍스트 없는 것(서브메뉴 스크롤)
                main_menu = search_result[0].find_elements(By.XPATH, "./div[not(@class) or @class='']")
                if "스폰서" in main_menu[0].get_attribute("innerText"):
                    main_menu[1].click()
                else:
                    main_menu[0].click()
                #리뷰클릭
                time.sleep(2)
                review_btn = driver.find_element(By.CSS_SELECTOR, "#QA0Szd > div > div > div.w6VYqd > div.bJzME.Hu9e2e.tTVLSc > div > div.e07Vkf.kA9KIf > div > div > div.m6QErb.DxyBCb.kA9KIf.dS8AEf.XiKgde > div:nth-child(3) > div > div > button:nth-child(2)")
                review_btn.click()

                scroll_el = 'document.querySelector("#QA0Szd > div > div > div.w6VYqd > div.bJzME.Hu9e2e.tTVLSc > div > div.e07Vkf.kA9KIf > div > div > div.m6QErb.DxyBCb.kA9KIf.dS8AEf.XiKgde")'
                
        else :
            #검색결과 한개 or 없을때
            try:
                review_btn = driver.find_element(By.CSS_SELECTOR, "#QA0Szd > div > div > div.w6VYqd > div:nth-child(2) > div > div.e07Vkf.kA9KIf > div > div > div:nth-child(3) > div > div > button:nth-child(2)")
                #리뷰클릭
                review_btn.click()
                
                scroll_el = 'document.querySelector("#QA0Szd > div > div > div.w6VYqd > div:nth-child(2) > div > div.e07Vkf.kA9KIf > div > div > div.m6QErb.DxyBCb.kA9KIf.dS8AEf.XiKgde")'

                #메인메뉴 스크롤
            except:
                #리뷰버튼 없음
                print("리뷰버튼 없음 ㅋㅋ")
                continue

    except Exception as e:
        print(e)
    
    time.sleep(2)

    score = driver.find_element(By.CSS_SELECTOR, ".fontDisplayLarge").text
    print(score)

    reviews = None

    total_reviews = driver.find_elements(By.CLASS_NAME, "jANrlb>div")[2].text
    total_reviews = int(re.sub(r"[^0-9\s]", "", total_reviews))
    time.sleep(2)
        
    while True:
        print("while works!")
        reviews = driver.find_elements(By.CLASS_NAME, "jftiEf")
        height = driver.execute_script(f"return {scroll_el}.scrollHeight")
        driver.execute_script(f"{scroll_el}.scrollTo(0, {scroll_el}.scrollHeight)")
        time.sleep(2)
        new_heigth = driver.execute_script(f"return {scroll_el}.scrollHeight")
        if len(reviews) < 5:
            if total_reviews == len(reviews):
                break
        else:
            if len(reviews) >= 5:
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
