import pymysql
import sys
sys.path.append(".")

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
        sql = "select * from view_list where uno=%s"
        self.cursor.execute(sql, (uno))
        
        #uno, sno 말고 얘 전용 no값이나 create_date 값이 있어야 그걸 바탕으로 나중에 들어온 5개를 가져올 수 있는 거 아닌가? 일단 보류!