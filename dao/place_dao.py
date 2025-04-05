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
    def search_places(self, q):
        sql = "select * from place where title like CONCAT('%%', %s, '%%') or sigungu like CONCAT('%%', %s, '%%')"
        self.cursor.execute(sql, (q, q))
        result = self.cursor.fetchall()
        places = []
        for place in result:
            contentid, overview, homepage, addr1, cat1, cat2, cat3, firstimage, mapx, mapy, title, sigungu = place
            vo = PlaceVO(contentid, overview, homepage, addr1, cat1, cat2, cat3, firstimage, mapx, mapy, title, sigungu)
            places.append(vo)
        return places

    #목록 조회
    def get_all_place(self, id, regions=None, page=0):
        
        if id :
            sql = "select place.*, IF(favorites.id = %s, 'TRUE', 'FALSE') AS checked from place left join favorites on place.contentid = favorites.contentid"
            if regions:
                if "기타" in regions:
                    sql += f" where sigungu in('무주군', '진안군', '장수군', {regions})"
                else:
                    sql += f" where sigungu in({regions})"
            sql += f" limit {page}, 10"
            # sql += " order..."
            self.cursor.execute(sql, (id))
        else:
            sql = "select *, 'False' as checked from place"
            if regions:
                sql += f" where sigungu in({regions})"
            sql += f" limit {page}, 10"
            self.cursor.execute(sql)

        result = self.cursor.fetchall()
        places = []
        for place in result:
            contentid, overview, homepage, addr1, cat1, cat2, cat3, firstimage, mapx, mapy, title, sigungu, checked = place
            
            vo = PlaceVO(contentid, overview, homepage, addr1, cat1, cat2, cat3, firstimage, mapx, mapy, title, sigungu, checked)
            places.append(vo)
        return places
    
    #단건 조회(post)
    def get_one_place(self, contentid):
        sql = "select * from place where contentid = %s"
        self.cursor.execute(sql, (contentid))
        result = self.cursor.fetchone()
        if result:
            contentid, overview, homepage, addr1, cat1, cat2, cat3, firstimage, mapx, mapy, title, sigungu = result
            return PlaceVO(contentid, overview, homepage, addr1, cat1, cat2, cat3, firstimage, mapx, mapy, title, sigungu)
        else:
            return None
