from favorites_dao import FavoritesDao
from user_dao import UserDAO
from vo.user_vo import UserVO
dao = UserDAO()
vo = UserVO()
vo = dao.get_one_user("hong")
print(vo.id)