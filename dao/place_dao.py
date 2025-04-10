import pymysql
import sys
sys.path.append(".")
from vo.place_vo import PlaceVO
from haversine import haversine
from itertools import permutations

class PlaceDAO:
    def __init__(self):
        self.conn = pymysql.connect(
            host="***REMOVED***",
            port=3306,
            user="milk",
            password="***REMOVED***",
            database="hotplace"
        )
        self.cursor = self.conn.cursor()
        print("쿼리 객체 생성")

    #인기순 조회
    def popularity_places(self):
        sql = "select * from place order by total_score asc limit 10"
        self.cursor.execute(sql)

        result = self.cursor.fetchall()
        places = []
        for place in result:
            contentid, overview, homepage, addr1, cat1, cat2, cat3, firstimage, mapx, mapy, title, sigungu, total_score= place
            
            vo = PlaceVO(contentid, overview, homepage, addr1, cat1, cat2, cat3, firstimage, mapx, mapy, title, sigungu, total_score)
            places.append(vo)
        return places


    #검색 조회
    def search_places(self, id, search=None, page=0):
        if id:
            sql = "select place.*, IF(favorites.id = %s, 'TRUE', 'FALSE') AS checked from place left join favorites on place.contentid = favorites.contentid"
            if search:
                sql += f" where title like CONCAT('%%', '{search}', '%%') or sigungu like CONCAT('%%', '{search}', '%%')"
            sql += f" limit {page}, 10"
            self.cursor.execute(sql, (id))
        else:
            sql = "select *, 'False' as checked from place"
            if search:
                sql += f" where title like CONCAT('%%', '{search}', '%%') or sigungu like CONCAT('%%', '{search}', '%%')"
            sql += f" limit {page}, 10"
            self.cursor.execute(sql)
        
        result = self.cursor.fetchall()
        places = []
        for place in result:
            contentid, overview, homepage, addr1, cat1, cat2, cat3, firstimage, mapx, mapy, title, sigungu, total_score, checked = place
            
            vo = PlaceVO(contentid, overview, homepage, addr1, cat1, cat2, cat3, firstimage, mapx, mapy, title, sigungu, total_score, checked)
            places.append(vo)
        return places
    
    #단건 조회(post)
    def get_one_place(self, contentid):
        sql = "select * from place where contentid = %s"
        self.cursor.execute(sql, (contentid))
        result = self.cursor.fetchone()
        if result:
            contentid, overview, homepage, addr1, cat1, cat2, cat3, firstimage, mapx, mapy, title, sigungu, total_score = result
            return PlaceVO(contentid, overview, homepage, addr1, cat1, cat2, cat3, firstimage, mapx, mapy, title, sigungu, total_score)
        else:
            return None

    #목록 조회(지역별)
    def get_all_place(self, id, regions=None, page=0, search=None):
        
        if id :
            sql = "select place.*, IF(favorites.id = %s, 'TRUE', 'FALSE') AS checked from place left join favorites on place.contentid = favorites.contentid and favorites.id = %s"
            if regions:
                if "기타" in regions:
                    sql += f" where sigungu in('무주군', '진안군', '장수군', {regions})"
                else:
                    sql += f" where sigungu in({regions})"
            if search:
                sql += f" where title like CONCAT('%%', '{search}','%%') or sigungu like CONCAT('%%', '{search}','%%')"
            sql += f" order by total_score desc limit {page}, 10"
            # sql += " order..."
            print(sql)
            self.cursor.execute(sql, (id, id))
        else:
            sql = "select *, 'False' as checked from place"
            if regions:
                sql += f" where sigungu in({regions})"
            if search:
                sql += f" where title like CONCAT('%%', '{search}','%%') or sigungu like CONCAT('%%', '{search}','%%')"
            sql += f" order by total_score desc limit {page}, 10"
            print(sql)
            self.cursor.execute(sql)

        result = self.cursor.fetchall()
        places = []
        for place in result:
            contentid, overview, homepage, addr1, cat1, cat2, cat3, firstimage, mapx, mapy, title, sigungu, total_score, checked = place
            
            vo = PlaceVO(contentid, overview, homepage, addr1, cat1, cat2, cat3, firstimage, mapx, mapy, title, sigungu, total_score, checked)
            places.append(vo)
        return places
    
    #목록 조회(테마별)
    def get_theme_place(self, id, cat=None, page=0, search=None):
        if id :
            sql = "select place.*, IF(favorites.id = %s, 'TRUE', 'FALSE') AS checked from place left join favorites on place.contentid = favorites.contentid and favorites.id = %s"
            if cat:
                sql += f" where cat2 in({cat})"
            if search:
                sql += f" where title like CONCAT('%%', '{search}','%%') or sigungu like CONCAT('%%', '{search}','%%')"
            sql += f" order by total_score desc limit {page}, 10"
            
            self.cursor.execute(sql, (id, id))
        else:
            sql = "select *, 'False' as checked from place"
            if cat:
                sql += f" where cat2 in({cat})"
            if search:
                sql += f" where title like CONCAT('%%', '{search}','%%') or sigungu like CONCAT('%%', '{search}','%%')"    
            sql += f" order by total_score desc limit limit {page}, 10"
            self.cursor.execute(sql)

        result = self.cursor.fetchall()
        places = []
        for place in result:
            contentid, overview, homepage, addr1, cat1, cat2, cat3, firstimage, mapx, mapy, title, sigungu, total_score, checked = place
            
            vo = PlaceVO(contentid, overview, homepage, addr1, cat1, cat2, cat3, firstimage, mapx, mapy, title, sigungu, total_score, checked)
            places.append(vo)
        return places
    
    #지역별 관광지 갯수 조회
    def get_count_region(self, regions=None, search=None):
        #region, theme
        sql = "select count(*) as cnt from place"
        if regions:
            sql += f" where sigungu in({regions})"
        if search:
            sql += f" where title like CONCAT('%%', '{search}','%%') or sigungu like CONCAT('%%', '{search}','%%')"
        self.cursor.execute(sql)
        result = self.cursor.fetchone()
        return result
        
    #테마별 관광지 갯수 조회
    def get_count_theme(self, theme=None, search=None):
        sql = "select count(*) as cnt from place"
        if theme:
            sql += f" where cat2 in({theme})"
        if search:
            sql += f" where title like CONCAT('%%', '{search}','%%') or sigungu like CONCAT('%%', '{search}','%%')"
        self.cursor.execute(sql)
        result = self.cursor.fetchone()
        return result
        
    #검색 관광지 갯수 조회
    def get_count_search(self, search=None):
        sql = "select count(*) as cnt from place"
        if search:
            sql += f" where title like CONCAT('%%', '{search}','%%') or sigungu like CONCAT('%%', '{search}','%%')"
        self.cursor.execute(sql)
        result = self.cursor.fetchone()
        return result
    
    #여행 코스 조회
    def get_course_place(self, region=None, cat=None):
        #select p.* from place p left join review r on p.contentid = r.contentid where sigungu = '전주시' and cat2 in('A0101') order by r.total_score desc;
        sql = "select * from place"

        if "기타" in region:
            sql += f" where sigungu in('무주군', '진안군', '장수군')"
        else:
            sql += f" where sigungu = '{region}'"

        if cat:
            sql += f" and cat2 in({cat}) order by total_score desc limit 3"
            self.cursor.execute(sql)
        else:
            sql += " limit 3"
            self.cursor.execute(sql)

        result = self.cursor.fetchall()
        courses = []
        for course in result:
            contentid, overview, homepage, addr1, cat1, cat2, cat3, firstimage, mapx, mapy, title, sigungu, total_score = course
            
            vo = PlaceVO(contentid, overview, homepage, addr1, cat1, cat2, cat3, firstimage, mapx, mapy, title, sigungu, total_score)
            courses.append(vo)
        if courses:
            return courses
        else:
            return None


    #경로탐색 기반 거리 조회
    def path(self, contentid):
        
        sql = """
            SELECT 
                pl.contentid, 
                pl.title, 
                pl.mapx, 
                pl.mapy, 
                p.contentid AS p_contentid, 
                p.title AS p_title, 
                p.firstimage as p_image,
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
        self.cursor.execute(sql, (contentid))
        desc = self.cursor.description
        column_names = [col[0] for col in desc]
        result = [dict(zip(column_names, row))  for row in self.cursor.fetchall()]
        
        print(result)


        # 3. 출발지: 가력도항
        # start = {
        #     "title": result[0]["title"],
        #     "mapx": result[0]["mapx"],
        #     "mapy": result[0]["mapy"]
        # }

        # 4. 두 번째 장소: 가장 가까운 장소
        second = {
            "title": result[0]["p_title"],
            "mapx": result[0]["p_mapx"],
            "mapy": result[0]["p_mapy"],
            "sigungu" : result[0]["p_sigungu"],
            "firstimage" : result[0]["p_image"],
            "cat2" : result[0]["p_cat2"],
            "contentid" : result[0]["p_contentid"]
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
                    "mapy": row["p_mapy"],
                    "sigungu" : row["p_sigungu"],
                    "firstimage" : row["p_image"],
                    "cat2" : row["p_cat2"],
                    "contentid" : row["p_contentid"]
                })
                used.add(row['p_contentid'])

        # 6. 최단 경로 탐색
        min_path = None
        min_total = float("inf")

        for perm in permutations(others):
            path = [second] + list(perm)
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
                "sigungu" : p["sigungu"],
                "firstimage" : p["firstimage"],
                "cat2" : p["cat2"],
                "contentid" : p["contentid"]
            }

            if i == 0:
                output["distance_from_prev"] = 0.0
                #print(f"{i+1}. {p['title']} | 좌표: ({p['mapx']}, {p['mapy']}) | 출발지")
            else:
                prev = min_path[i - 1]
                d = haversine((prev["mapy"], prev["mapx"]), (p["mapy"], p["mapx"]))
                output["distance_from_prev"] = round(d, 2)
                #print(f"{i+1}. {p['title']} | 좌표: ({p['mapx']}, {p['mapy']}) | 이전 거리: {d:.2f} km")

            final_result.append(output)
        #print(f"\n총 거리: {min_total:.2f} km")
        return final_result