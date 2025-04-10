import requests

# Kakao Mobility API 키
api_key = "KaKaoAK ${***REMOVED***}"  # "KakaoAK " 뒤에 띄어쓰기 반드시 포함

# 요청 URL
url = "https://apis-navi.kakaomobility.com/v1/waypoints/directions"

# 쿼리 파라미터
params = {
    "origin": "127.712424,35.965129",
    "waypoints" : "127.680078,35.920581|127.589582,35.680518",
    "destination": "127.694148,35.851997",
    "waypoints": "127.17354989857544,37.36629687436494",
}

# 헤더
headers = {
    "Authorization": api_key,
    "Content-Type": "application/json"
}

# GET 요청
response = requests.get(url, headers=headers, params=params)

# 결과 출력
if response.status_code == 200:
    data = response.json()
    print("요청 성공:")
    print(data)
else:
    print(f"요청 실패. 상태 코드: {response.status_code}")
    print(response.text)