import requests
import pandas as pd
import json

url = "http://apis.data.go.kr/B551011/KorService1/areaBasedList1"
decoding_key = "URTswZPeOQXXKFV5I515RLvkfr9wr6y7pyhhez9kacQjyQWrbAjjyn5I9V9pwaYQNYWxZu7gyOeMSCvXqoYJEQ=="

res = []

for i in range(1, 12):
    params = {
        "serviceKey" : decoding_key,
        "_type" : "json",
        "pageNo" : i,
        "contentTypeId" : "12",
        "numOfRows" : "100",
        "MobileOS" : "WIN",
        "MobileApp" : "Hotplace",
        "areaCode" : "37"
    }	

    response = requests.get(url, params=params).json()
        
    datas = response["response"]["body"]["items"]["item"]

    for data in datas:
        res.append(data)
        
print(res)
 
df = pd.DataFrame(res)
print(df.head())

df.to_csv("datas/region.csv", index=False)