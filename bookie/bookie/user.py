from silverlib.user import UserBase


class User(UserBase):
 
    def __init__(self, name):
        UserBase.__init__(self, name)
        self.is_admin = False
        self.email_address = ""

