from dotenv import load_dotenv
load_dotenv()
import os
from haversine import haversine
from itertools import permutations
import pymysql

# 1. MySQL 연결
conn = pymysql.connect(
    host=os.getenv("DB_HOST"),
    port=3306,
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database="hotplace"
)
cursor = conn.cursor(pymysql.cursors.DictCursor)

# 2. 쿼리 실행 (원본 그대로 사용)
sql = """
SELECT 
    pl.contentid, 
    pl.title, 
    pl.mapx, 
    pl.mapy, 
    p.contentid AS p_contentid, 
    p.title AS p_title, 
    p.firstimage,
    p.cat2 AS p_cat2,
    p.sigungu AS p_sigungu,
    p.mapx AS p_mapx, 
    p.mapy AS p_mapy, 
    (SELECT ST_DISTANCE_SPHERE(POINT(pl.mapx, pl.mapy), POINT(p.mapx, p.mapy)) / 1000) AS dist 
FROM place pl 
INNER JOIN similar s ON pl.contentid = s.no 
INNER JOIN place p ON p.contentid = s.sno 
WHERE pl.contentid = %s 
ORDER BY dist
"""
cursor.execute(sql, (2743285,))
result = cursor.fetchall()

# 3. 출발지: 가력도항
start = {
    "title": result[0]["title"],
    "mapx": result[0]["mapx"],
    "mapy": result[0]["mapy"]
}

# 4. 두 번째 장소: 가장 가까운 장소
second = {
    "title": result[0]["p_title"],
    "mapx": result[0]["p_mapx"],
    "mapy": result[0]["p_mapy"]
}

# 5. 나머지 장소 구성 (중복 제거)
others = []
used = set()
used.add(result[0]['p_contentid'])

for row in result[1:]:
    if row['p_contentid'] not in used:
        others.append({
            "title": row["p_title"],
            "mapx": row["p_mapx"],
            "mapy": row["p_mapy"]
        })
        used.add(row['p_contentid'])

# 6. 최단 경로 탐색
min_path = None
min_total = float("inf")

for perm in permutations(others):
    path = [start, second] + list(perm)
    dist = 0
    for i in range(len(path) - 1):
        a = (path[i]["mapy"], path[i]["mapx"])
        b = (path[i+1]["mapy"], path[i+1]["mapx"])
        dist += haversine(a, b)
    if dist < min_total:
        min_total = dist
        min_path = path

# 7. 결과 저장 및 출력
final_result = []
print("방문 순서:")
for i, p in enumerate(min_path):
    output = {
        "order": i + 1,
        "title": p["title"],
        "mapx": p["mapx"],
        "mapy": p["mapy"],
        "cat2" : p["cat2"],
        "firstimage" : p["firstimage"],
        "sigungu" : p["sigungu"]
    }

    if i == 0:
        output["distance_from_prev"] = 0.0
        print(f"{i+1}. {p['title']} | 좌표: ({p['mapx']}, {p['mapy']}) | 출발지")
    else:
        prev = min_path[i - 1]
        d = haversine((prev["mapy"], prev["mapx"]), (p["mapy"], p["mapx"]))
        output["distance_from_prev"] = round(d, 2)
        print(f"{i+1}. {p['title']} | 좌표: ({p['mapx']}, {p['mapy']}) | 이전 거리: {d:.2f} km")

    final_result.append(output)
print(final_result)
# print(f"\n총 거리: {min_total:.2f} km")