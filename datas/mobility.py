import requests
import json
import pymysql
from haversine import haversine

# def get_directions(api_key, origin, destination):
#     url = "https://apis-navi.kakaomobility.com/v1/waypoints/directions"
    
#     #파라미터
#     params = {
#         ""
#     }

# import requests

# # Kakao Mobility API 키
# api_key = "KakaoAK ***REMOVED***"  # "KakaoAK " 뒤에 띄어쓰기 반드시 포함

# # 요청 URL
# url = "https://apis-navi.kakaomobility.com/v1/directions"

# # 쿼리 파라미터
# params = {
#     "origin": "127.712424,35.965129",
#     "waypoints" : "127.680078,35.920581|127.589582,35.680518",
#     "destination": "127.694148,35.851997",
# }

# # 헤더
# headers = {
#     "Authorization": api_key,
#     "Content-Type": "application/json"
# }

# # GET 요청
# response = requests.get(url, headers=headers, params=params)

# # 결과 출력
# if response.status_code == 200:
#     data = response.json()
#     print("요청 성공:")
#     print(data)
# else:
#     print(f"요청 실패. 상태 코드: {response.status_code}")
#     print(response.text)



conn = pymysql.connect(
    host="***REMOVED***",
    port=3306,
    user="milk",
    password="***REMOVED***",
    database="hotplace"
)
cursor = conn.cursor(pymysql.cursors.DictCursor)

sql = """select 
	pl.contentid, 
	pl.title, 
	pl.mapx, 
	pl.mapy, 
	p.contentid, 
	p.title, 
	p.firstimage, 
	p.mapx, 
	p.mapy, 
	(SELECT ST_DISTANCE_SPHERE(point(pl.mapx, pl.mapy), point(p.mapx,p.mapy)) / 1000) as dist 
from place pl 
	inner join similar s on pl.contentid = s.no 
	inner join place p on p.contentid = s.sno 
where pl.contentid = %s order by dist"""

no = 2743285

cursor.execute(sql, (no))
result = cursor.fetchall()

print(result)

location_dict = {}

for i, locations in enumerate(result):
    
    location_list = []
    
    for location in result:
        #print(location.keys())
        #기준 위치:
        #print("기준위치", result[i])
        #타겟 위치
        #print("타겟위치", location)
        base = (result[i]["p.mapy"], result[i]["p.mapx"])
        #print(base)
        target = (location["p.mapy"], location["p.mapx"])
        data = haversine(base, target)
        print(f'{result[i]["p.title"]} > {location["p.title"]}')
        print(data)
        
        dist_dict = {
            
            "target" : location["p.title"],
            "dist" : data
        }
        location_list.append(dist_dict)
    location_dict[result[i]["p.title"]] = location_list
        
        
print(location_dict)