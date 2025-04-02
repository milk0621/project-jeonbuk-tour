import pymysql
import sys
sys.path.append(".")
from vo.place_vo import PlaceVO

class PlaceDao:
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
        sql = "select * form place where title like %s" #or 지역명 like %s
        self.cursor.execute(sql, (q))
        result = self.cursor.fetchall()
        places = []
        for place in result:
            contentid, overview, homepage, addr1, cat1, cat2, cat3, firstimage, mapx, mapy, title, sigungu = result
            vo = PlaceVO(contentid, overview, homepage, addr1, cat1, cat2, cat3, firstimage, mapx, mapy, title, sigungu)
            places.append(vo)
        return places

    #목록 조회
    def get_all_place(self):
        sql = "select * from place limit 5"
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        places = []
        for place in result:
            contentid, overview, homepage, addr1, cat1, cat2, cat3, firstimage, mapx, mapy, title, sigungu = place
            vo = PlaceVO(contentid, overview, homepage, addr1, cat1, cat2, cat3, firstimage, mapx, mapy, title, sigungu)
            places.append(vo)
        return places
    
    #단건 조회(post)
    def get_one_place(self, no):
        sql = "select * from place where no = %s"
        self.cursor.execute(sql, (no))
        result = self.cursor.fetchone()
        if result:
            contentid, overview, homepage, addr1, cat1, cat2, cat3, firstimage, mapx, mapy, title, sigungu = result
            return PlaceVO(contentid, overview, homepage, addr1, cat1, cat2, cat3, firstimage, mapx, mapy, title, sigungu)
        else:
            return None
