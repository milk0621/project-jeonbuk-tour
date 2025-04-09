import pymysql
import sys
import random
sys.path.append(".")
from vo.favorites_vo import FavoritesVO
from vo.place_vo import PlaceVO

class FavoritesDAO:
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

    #추가
    def insert_favorite(self, id, contentid):
        sql = "insert into favorites(id, contentid)values(%s, %s)"
        print(sql)
        self.cursor.execute(sql, (id, contentid))
        self.conn.commit()

    #삭제
    def delete_favorite(self, id, contentid):
        sql = "delete from favorites where id = %s and contentid = %s"
        self.cursor.execute(sql, (id, contentid))
        self.conn.commit()

    #조회
    def selecte_favorite(self, id):
        sql = "select p.* from favorites f left join place p on f.contentid = p.contentid where f.id = %s"
        #select * from favorites f left join place p on f.contentid = p.contentid where f.id = 'hong';
        
        self.cursor.execute(sql, (id))
        result = self.cursor.fetchall()
        favorites = []
        for favorite in result:
            contentid, overview, homepage, addr1, cat1, cat2, cat3, firstimage, mapx, mapy, title, sigungu, total_score = favorite
            
            vo = PlaceVO(contentid, overview, homepage, addr1, cat1, cat2, cat3, firstimage, mapx, mapy, title, sigungu, total_score)
            favorites.append(vo)
        return favorites

    #유사도 조회 후 랜덤조회
    def random(self, contentids):
        sql = f"select distinct p2.* from place p left join `similar` s on s.no = p.contentid  left join place p2 on s.sno = p2.contentid where p.contentid in({', '.join(contentids)}) order by rand() limit 5;"
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        # random.shuffle(all_contentids)
        return results
    
    def close(self):
        self.cursor.close()
        self.conn.close()

