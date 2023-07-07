from creditcard import CreditCard as CreditCardValidator
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class CreditCard(db.Model):
    __tablename__ = "creditcards"

    id = db.Column(db.Integer, primary_key=True)
    holder = db.Column(db.String, nullable=False)
    number = db.Column(db.String, nullable=False)
    exp_date = db.Column(db.Date, nullable=False)
    cvv = db.Column(db.String)
    brand = db.Column(db.String)

    def __init__(self, holder, number, exp_date, cvv=None):
        self.holder = holder
        self.number = number
        self.exp_date = exp_date
        self.cvv = cvv
        self.brand = self.get_brand(number)

    @staticmethod
    def get_brand(number):
        cc = CreditCardValidator(number)
        return cc.get_brand()
