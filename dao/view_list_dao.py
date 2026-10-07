import os
import pymysql
import sys
sys.path.append(".")
from vo.view_list_vo import ViewlistVO
from vo.place_vo import PlaceVO

class ViewlistDAO:
    def __init__(self):
        self.conn = pymysql.connect(
            host=os.getenv("DB_HOST"),
            port=3306,
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database="hotplace"
        )
        self.cursor = self.conn.cursor()
    
    #추가
    def insert_view_list(self, id, sno):
        sql = "insert into view_list(id, sno)values(%s, %s)"
        self.cursor.execute(sql, (id, sno))
        self.conn.commit()

    #조회
    def select_view_list(self, id):
        sql = "select p.*, IF(f.id = %s, 'TRUE', 'FALSE') AS checked from view_list v left join place p on v.sno = p.contentid left join favorites f on p.contentid = f.contentid where v.id = %s order by no desc limit 5"
        self.cursor.execute(sql, (id, id))
        result = self.cursor.fetchall()
        view_lists = []
        for view_list in result:
            contentid, overview, homepage, addr1, cat1, cat2, cat3, firstimage, mapx, mapy, title, sigungu, total_score, checked = view_list
            
            vo = PlaceVO(contentid, overview, homepage, addr1, cat1, cat2, cat3, firstimage, mapx, mapy, title, sigungu, total_score, checked)
            view_lists.append(vo)
        return view_lists
            
        