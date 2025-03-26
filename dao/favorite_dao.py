import pymysql
import sys
sys.path.append(".")
from vo.favorite_vo import FavoriteVO

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
        sql = "insert into favorite(uno, sno)values(%s, %s)"
        self.cursor.execute(sql, (uno, sno))
        self.conn.commit()

    #삭제
    def delete_favorite(self, uno):
        sql = "delete from favorite where uno = %s"
        self.cursor.execute(sql, (uno))
        self.conn.commit()

    def close(self):
        self.cursor.close()
        self.conn.close()


