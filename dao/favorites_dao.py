import pymysql
import sys
sys.path.append(".")
from vo.favorites_vo import FavoritesVO

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
        sql = "select * from favorites where id = %s"
        self.cursor.execute(sql, (id))
        result = self.cursor.fetchall()
        favorites = []
        for favorite in result:
            id, contentid = favorite
            vo = FavoritesVO(id, contentid)
            favorites.append(vo)
        return favorites

    def close(self):
        self.cursor.close()
        self.conn.close()

