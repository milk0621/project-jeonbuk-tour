import requests
import pandas as pd
import json

url = "http://apis.data.go.kr/B551011/KorService1/detailIntro1"
decoding_key = "PGarApfpuY1YOjiqqzSf2rDH0jRgz4DG7JPgm2Une6+Y/IyWCjPB/kO+JGiqs3Od4iX9JZpHs7BU4YAHzv/9nQ=="

df = pd.read_csv("datas/region.csv")
contentid = df["contentid"]
print(contentid)

res = []
for c in contentid:
    params = {
        "numOfRows" : "1",
        "pageNo" : "1",
        "MobileOS" : "WIN",
        "MobileApp" : "Hotplace",
        "serviceKey" : decoding_key,
        "_type" : "json",
        "contentId" : c,
        "contentTypeId" : "12"
    }	
    
    response = requests.get(url, params=params).json()
    data = response["response"]["body"]["items"]["item"]

    res.append(data)
    print(res)

df2 = pd.DataFrame(res)

df2.to_csv("datas/region_post.csv")