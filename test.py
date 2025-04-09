from dao.favorites_dao import FavoritesDAO
dao = FavoritesDAO()
contentids = [125415, 125416, 125447]
dao.random(contentids)
