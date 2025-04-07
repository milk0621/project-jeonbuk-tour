import re
import pandas as pd
from konlpy.tag import Okt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

df = pd.read_csv("./datas/pre_region_data.csv")
df2 = pd.read_csv("./datas/review_groub.csv")

result = pd.merge(df, df2, how='left', on='title')
# print(result.head())

title = result["title"]
content = result["overview"]
contentid = result["contentid"]

cat1 = result["cat1"]
cat2 = result["cat2"]
cat3 = result["cat3"]

review = result["review"]

result["total"] = title + " " + content + " " + cat1.astype(str) + " " + cat2.astype(str) + " " + cat3.astype(str) + " " + review.astype(str)

print(result["total"].head())


stop = pd.read_csv("./datas/stopwords.txt")
# print(df["total"])

okt = Okt()
stopwords = stop.to_numpy().reshape(1, -1)[0]
#1행 595열(2차원)의 0번째인덱스

def clean_text(text):
  #한글, 숫자만 남기고 나머지 제거
  text = re.sub(r"[^ㄱ-ㅎ가-힣0-9a-zA-Z\s]", " ", text)
  #ㄱ-ㅎ가-힣0-9를 제외한 나머지 모든 문자를 " "띄어쓰기로 치환

  text = text.replace("\r", " ").replace("\n", " ")
  
  #띄어쓰기가 두개 이상인경우 하나로 치환
  text = re.sub(r"\s+", " ", text)

  #양쪽 공백 제거
  text = text.strip()
  #"       안녕하세요 저는 ~~~ 입니다.     " -> "안녕하세요 저는 ~~~ 입니다."

  #형태소 단위로 분석(쪼개기), 어간추출(뛰었다 -> 뛰다)
  tokens = okt.morphs(text, stem=True)
  #안녕하세요 저는 홍길동 입니다 -> ["안녕", "하세요", "저는", "홍길동", "입니다"]

  #불용어 제거
  tokens = [token for token in tokens if token not in stopwords]
  #["안녕", "하세요", "저는", "홍길동", "입니다"] -> ["안녕", "하세요", "홍길동", "입니다"]

  #리스트를 문자열로 변환
  #["안녕", "하세요", "홍길동", "입니다"] -> "안녕 하세요 홍길동 입니다"

  return " ".join(tokens)

result["total"] = result["total"].apply(clean_text)

print(result.head())

vectorizer = TfidfVectorizer(stop_words="english")

tour_vec = vectorizer.fit_transform(result["total"])

# print(vectorizer.get_feature_names_out())

# print(tour_vec[:5])

#단어사전 길이만큼의 열
#여행지 개수 만큼의 행
#[0. 0.1 0. 0. 0.5 ....]

#여행지 개수만큼의 열
#여행지 개수만큼의 행
#[0. 0.1 0. 0. 0.5 ....]
sim_matrix = cosine_similarity(tour_vec, tour_vec)

recommend_region = []

#상위 n개 유사한 광고 출력
for idx, sim_row in enumerate(sim_matrix):
  #유사도 오름차순 정렬
  #낮은것 -> 높은것
  
  #i번째 관광지의
#   print(df.loc[idx, "contentid"]) #가력도항 id
#   print(df.loc[idx, "title"]) #가력도항
  
  
  #내림차순 정렬 (인덱스)
  top = sim_row.argsort()[::-1][1:6]
  #유사도 내림차순 정렬
  for i in top:
    #내림차순 정렬된 인덱스를 순회
    # print(df.loc[i, "contentid"]) #가력도항 비슷한 궁항 id, 선유1구항 id, 야미도선착장 id ...
    # print("="*20)
    # print(df.loc[i, "title"], sim_row[i]) #가력도항 비슷한 궁항, 선유1구항, 야미도선착장
    
    recommend_region.append({
        "contentid1" : result.loc[idx, "contentid"], 
        "contentid2" : result.loc[i, "contentid"],
        "sim" : sim_row[i]
        }
    )
    
df2= pd.DataFrame(recommend_region)
    
df2.to_csv("./datas/recommend_region2.csv", index=False)
