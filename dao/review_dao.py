import pymysql
import sys
sys.path.append(".")
from vo.review_vo import ReviewVO

class ReviewDAO:
    def __init__(self):
        self.conn = pymysql.connect(
            host="***REMOVED***",
            port=3306,
            user="milk",
            password="***REMOVED***",
            database="hotplace"
        )
        self.cursor = self.conn.cursor()

    #전체 조회
    def select_review(self, contentid):
        sql = "select * from review where contentid = %s"
        self.cursor.execute(sql, (contentid))
        result = self.cursor.fetchall()
        reviews = []
        for review in result:
            contentid, name, review, score = review
            vo = ReviewVO(contentid, name, review, score)
            reviews.append(vo)

        if result:
            return reviews
        else:
            return None
    

