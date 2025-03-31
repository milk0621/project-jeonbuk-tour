import pymysql
import sys
sys.path.append(".")
from vo.review_vo import ReviewVO

class ReviewDao:
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
    def select_review(self, sno):
        sql = "select * from review where sno = %s"
        self.cursor.execute(sql, (sno))
        result = self.cursor.fetchall()
        reviews = []
        for review in result:
            no, sno, star_score, author, content, score = review
            vo = ReviewVO(no, sno, star_score, author, content, score)
            reviews.append(vo)
        return reviews
