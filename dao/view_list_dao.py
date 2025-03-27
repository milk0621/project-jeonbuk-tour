import pymysql
import sys
sys.path.append(".")
from vo.view_list_vo import ViewlistVO

class ViewlistDao:
    def __init__(self):
        self.conn = pymysql.connect(
            host="***REMOVED***",
            port=3306,
            user="milk",
            password="***REMOVED***",
            database="hotplace"
        )
        self.cursor = self.conn.cursor()
    
    #추가
    def insert_view_list(self, uno, sno):
        sql = "insert into view_list(uno, sno)values(%s, %s)"
        self.cursor.execute(sql, (uno, sno))
        self.conn.commit()

    #조회
    def select_view_list(self, uno):
        sql = "select * from view_list order by 'no' desc limit 5 where uno=%s"
        self.cursor.execute(sql, (uno))
        result = self.cursor.fetchall()
        view_lists = []
        for view_list in result:
            no, uno, sno = view_list
            vo = ViewlistVO(no, uno, sno)
            view_lists.append(vo)
        return view_lists
            
        