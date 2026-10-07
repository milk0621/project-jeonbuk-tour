import os
import pymysql
import sys
sys.path.append(".")
from vo.review_vo import ReviewVO

class ReviewDAO:
    def __init__(self):
        self.conn = pymysql.connect(
            host=os.getenv("DB_HOST"),
            port=3306,
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
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
    

