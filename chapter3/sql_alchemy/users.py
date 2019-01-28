from ext import db
class User(db.Model):
    __tablename__ = 'users2'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50))
    mail = db.Column(db.String(100))
    def __init__(self, name ,mail):
        self.name = name
        self.mail = mail