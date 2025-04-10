import requests

def mobility(maps):
    # Kakao Mobility API 키
    api_key = "KakaoAK ***REMOVED***"  # "KakaoAK " 뒤에 띄어쓰기 반드시 포함

    # 요청 URL
    url = "https://apis-navi.kakaomobility.com/v1/directions"
    
    result = []

    for map in maps:
        print(map.place_vo)
        waypoint_list = []
        #["126.6937182056,35.950790920", "127.1289151382,35.9630442455"]
        for waypoint in map.place_vo[:2]:
            waypoint_list.append(f'{waypoint["mapx"]},{waypoint["mapy"]}')
        # 쿼리 파라미터
        params = {
            "alternatives" : True,
            #출발지
            "origin": f'{map.mapx},{map.mapy}',
            
            #경유지
            "waypoints" : "|".join(waypoint_list),

            #목적지
            "destination": f'{map.place_vo[2]["mapx"]},{map.place_vo[2]["mapy"]}'
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
            print(response.url)
            #print(data)
            result.append(data)
        else:
            print(f"요청 실패. 상태 코드: {response.status_code}")
            print(response.text)
    for a in result:
        print("@@@@@@@@@@@",a)
    return result