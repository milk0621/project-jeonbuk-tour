import pymysql
import sys
sys.path.append(".")
from vo.favorites_vo import FavoritesVO

class FavoriteDao:
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
    def insert_favorite(self, uno, sno):
        sql = "insert into favorites(uno, sno)values(%s, %s)"
        self.cursor.execute(sql, (uno, sno))
        self.conn.commit()

    #삭제
    def delete_favorite(self, uno):
        sql = "delete from favorites where uno = %s"
        self.cursor.execute(sql, (uno))
        self.conn.commit()

    def close(self):
        self.cursor.close()
        self.conn.close()

    #조회
    def selecte_favorite(self, uno):
        sql = "select * from favorites where uno = %s"
        self.cursor.execute(sql, (uno))
        result = self.cursor.fetchall()
        favorites = []
        for favorite in result:
            uno, sno = favorite
            vo = FavoritesVO(uno, sno)
            favorites.append(vo)
        return favorites


