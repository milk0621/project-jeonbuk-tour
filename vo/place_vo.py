class PlaceVO:
    def __init__(self, contentid=None, overview=None, homepage=None, addr1=None, cat1=None, cat2=None, cat3=None, firstimage=None, mapx=None, mapy=None, title=None, sigungu=None, checked=None):
        self.contentid = contentid
        self.overview = overview
        self.homepage = homepage
        self.addr1 = addr1
        self.cat1 = cat1
        self.cat2 = cat2
        self.cat3 = cat3
        self.firstimage = firstimage
        self.mapx = mapx
        self.mapy = mapy
        self.title = title
        self.sigungu = sigungu
        self.checked = checked

    #리스트 형식의 배열을 딕셔너리 형식으로 변환
    #Flask의 jsonify() 함수는 dict, list, str, int 등 JSON으로 직렬화할 수 있는 기본 타입만 받기 때문에 PlaceVO와 같은 사용자 정의 클래스는 에러가 발생.
    def to_dict(self):
        return {
            "contentid": self.contentid,
            "overview": self.overview,
            "homepage": self.homepage,
            "addr1": self.addr1,
            "cat1": self.cat1,
            "cat2": self.cat2,
            "cat3": self.cat3,
            "firstimage": self.firstimage,
            "mapx": self.mapx,
            "mapy": self.mapy,
            "title": self.title,
            "sigungu": self.sigungu,
            "checked": self.checked
        }