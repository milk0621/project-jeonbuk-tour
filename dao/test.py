from dao.user_dao import UserDAO

dao = UserDAO()
dao.join("hong", "1234", "홍길동", "hong@example.com")
