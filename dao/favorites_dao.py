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
    def insert_favorite(self, id, sno):
        sql = "insert into favorites(id, sno)values(%s, %s)"
        self.cursor.execute(sql, (id, sno))
        self.conn.commit()

    #삭제
    def delete_favorite(self, id):
        sql = "delete from favorites where id = %s"
        self.cursor.execute(sql, (id))
        self.conn.commit()

    def close(self):
        self.cursor.close()
        self.conn.close()

    #조회
    def selecte_favorite(self, id):
        sql = "select * from favorites where id = %s"
        self.cursor.execute(sql, (id))
        result = self.cursor.fetchall()
        favorites = []
        for favorite in result:
            id, sno = favorite
            vo = FavoritesVO(id, sno)
            favorites.append(vo)
        return favorites


