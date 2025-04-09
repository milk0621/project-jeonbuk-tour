import pymysql
import sys
sys.path.append(".")
from vo.place_vo import PlaceVO

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
            sql = "select place.*, IF(favorites.id = %s, 'TRUE', 'FALSE') AS checked from place left join favorites on place.contentid = favorites.contentid"
            if regions:
                if "기타" in regions:
                    sql += f" where sigungu in('무주군', '진안군', '장수군', {regions})"
                else:
                    sql += f" where sigungu in({regions})"
            if search:
                sql += f" where title like CONCAT('%%', '{search}','%%') or sigungu like CONCAT('%%', '{search}','%%')"
            sql += f" limit {page}, 10"
            # sql += " order..."
            print(sql)
            self.cursor.execute(sql, (id))
        else:
            sql = "select *, 'False' as checked from place"
            if regions:
                sql += f" where sigungu in({regions})"
            if search:
                sql += f" where title like CONCAT('%%', '{search}','%%') or sigungu like CONCAT('%%', '{search}','%%')"
            sql += f" limit {page}, 10"
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
            sql = "select place.*, IF(favorites.id = %s, 'TRUE', 'FALSE') AS checked from place left join favorites on place.contentid = favorites.contentid"
            if cat:
                sql += f" where cat2 in({cat})"
            if search:
                sql += f" where title like CONCAT('%%', '{search}','%%') or sigungu like CONCAT('%%', '{search}','%%')"
            sql += f" limit {page}, 10"
            
            self.cursor.execute(sql, (id))
        else:
            sql = "select *, 'False' as checked from place"
            if cat:
                sql += f" where cat2 in({cat})"
            if search:
                sql += f" where title like CONCAT('%%', '{search}','%%') or sigungu like CONCAT('%%', '{search}','%%')"    
            sql += f" limit {page}, 10"
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
            sql += f" where sigungu = {region}"

        if cat:
            sql += f" and cat2 in({cat}) order by total_score desc limit 5"
            self.cursor.execute(sql)
        else:
            sql += " limit 5"
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

