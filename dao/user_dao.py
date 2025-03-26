import pymysql
import sys
sys.path.append(".")
from vo.user_vo import UserVO

class UserDAO:
    def __init__(self):
        self.conn = pymysql.connect(
            host="***REMOVED***",
            port=3306,
            user="friendship",
            password="***REMOVED***",
            database="hotplace"
        )
        self.cursor = self.conn.cursor()
    
    #1. 회원가입
    def join(self, id, pw, name, email):
        sql = "insert into user(id, pw, name, email) values(%s, %s, %s, %s)"
        self.cursor.execute(sql, (id, pw, name, email))
        self.conn.commit()
    
    #2. 로그인
    def login(self, id, pw):
        sql = "select * from user where id = %s, pw = %s"
        self.cursor.execute(sql, (id, pw))
        result = self.cursor.fetchone()
        if result:
            no, id, pw, name, email = result