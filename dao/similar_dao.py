import pymysql
import sys
sys.path.append(".")
from vo.similar_vo import SimilerVO

class SimilarDAO:
    def __init__(self):
        self.conn = pymysql.connect(
            host="***REMOVED***",
            port=3306,
            user="milk",
            password="***REMOVED***",
            database="hotplace"
        )
        self.cursor = self.conn.cursor()
    
    #유사도 조회    
    def select_similar(self, no):
        sql = "select p.contentid, p.title, p.firstimage from place pl inner join similar s on pl.contentid = s.no inner join place p on p.contentid = s.sno where pl.contentid = %s order by similar desc limit 3"
        self.cursor.execute(sql, (no))
        result = self.cursor.fetchall()
        similars = []
        for similar in result:
            contentid, title, firstimage = similar
            vo = SimilerVO(contentid, title, firstimage)
            similars.append(vo)
        return similars
            