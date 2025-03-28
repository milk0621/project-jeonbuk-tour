import requests
import pandas as pd
import json

url = "http://apis.data.go.kr/B551011/KorService1/detailIntro1"
decoding_key = "URTswZPeOQXXKFV5I515RLvkfr9wr6y7pyhhez9kacQjyQWrbAjjyn5I9V9pwaYQNYWxZu7gyOeMSCvXqoYJEQ=="

df = pd.read_csv("datas/region.csv")
contentid = df["contentid"]
print(contentid)

# res = []
# for c in contentid:
#     params = {
#         "numOfRows" : "1",
#         "pageNo" : "1",
#         "MobileOS" : "WIN",
#         "MobileApp" : "Hotplace",
#         "serviceKey" : decoding_key,
#         "_type" : "json",
#         "contentId" : c,
#         "contentTypeId" : "12"
#     }	
    
#     response = requests.get(url, params=params)
#     print(response.text)
    # data = response["response"]["body"]["items"]["item"]

    # res.append(data)
    # print(res)

# df2 = pd.DataFrame(res)

# df2.to_csv("datas/region_post.csv")