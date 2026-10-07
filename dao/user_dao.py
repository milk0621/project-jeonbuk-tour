import os
import pymysql
import sys
sys.path.append(".")
from vo.user_vo import UserVO

class UserDAO:
    def __init__(self):
        self.conn = pymysql.connect(
            host=os.getenv("DB_HOST"),
            port=3306,
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
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
        sql = "select * from user where id = %s and pw = %s and user_type = 1"
        self.cursor.execute(sql, (id, pw))
        result = self.cursor.fetchone()
        return result
    
    #3. 회원조회(마이페이지)
    def get_one_user(self, id):
        sql = "select * from user where id = %s and user_type = 1"
        self.cursor.execute(sql, (id))
        result = self.cursor.fetchone()
        if result:
            id, pw, name, email, user_type, create_date, delete_date = result
            return UserVO(id, pw, name, email, user_type, create_date, delete_date)
        else:
            return None
        
    #4. 비밀번호변경
    def update_pw(self, id, pw):
        sql = "update user set pw = %s where id = %s"
        self.cursor.execute(sql, (pw, id))
        self.conn.commit()
        
    #5. 탈퇴
    def delete_user(self, id):
        sql = "update user set user_type = 99, delete_date = now() where id = %s"
        self.cursor.execute(sql, (id))
        self.conn.commit()