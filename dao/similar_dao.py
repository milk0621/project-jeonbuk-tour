import os
import pymysql
import sys
sys.path.append(".")
from vo.similar_vo import SimilerVO
from vo.place_vo import PlaceVO

class SimilarDAO:
    def __init__(self):
        self.conn = pymysql.connect(
            host=os.getenv("DB_HOST"),
            port=3306,
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database="hotplace"
        )
        self.cursor = self.conn.cursor()
    
    #유사도 조회    
    def select_similar(self, no):
        sql = "select p.contentid, p.title, p.firstimage, p.cat2, p.sigungu from place pl inner join similar s on pl.contentid = s.no inner join place p on p.contentid = s.sno where pl.contentid = %s order by sim desc limit 3"
        self.cursor.execute(sql, (no))
        result = self.cursor.fetchall()
        similars = []
        for similar in result:
            contentid, title, firstimage, cat2, sigungu = similar
            vo = SimilerVO(contentid, title, firstimage, cat2, sigungu)
            similars.append(vo)
        return similars

    # def select_similar(self, no):
    #     sql = "select p.* from place p left join similar s on p.contentid = s.no where s.no = %s order by sim desc limit 3"
    #     self.cursor.execute(sql, (no))
    #     result = self.cursor.fetchall()
    #     similars = []
    #     for similar in result:
    #         contentid, overview, homepage, addr1, cat1, cat2, cat3, firstimage, mapx, mapy, title, sigungu, total_score = similar
            
    #         vo = PlaceVO(contentid, overview, homepage, addr1, cat1, cat2, cat3, firstimage, mapx, mapy, title, sigungu, total_score)
    #         similars.append(vo)
    #     return similars
            