import requests

url = "http://apis.data.go.kr/B551011/KorService1/areaBasedList1"

params = {
    "serviceKey" : "URTswZPeOQXXKFV5I515RLvkfr9wr6y7pyhhez9kacQjyQWrbAjjyn5I9V9pwaYQNYWxZu7gyOeMSCvXqoYJEQ==",
    "_type" : "json",
    "pageNo" : "1",
    "numOfRows" : "100",
    "MobileOS" : "WIN",
    "MobileApp" : "Hotplace",
    "areaCode" : "37"
}	

response = requests.get(url, params=params)
print(response.text)