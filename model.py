person_col = ("person_id", "person_faceid", "person_name", "person_class_id", "person_pic")


# person表
class Person:

    def __init__(self,faceid,name,class_id,pic):
        self.id = 0
        self.faceid = faceid
        self.name = name
        self.class_id = class_id
        self.pic = pic