from calendar import monthrange
from datetime import datetime

from creditcard import CreditCard as CreditCardValidator

from card_vault.extensions import db
from card_vault.utils import AESCipher


class CreditCard(db.Model):
    __tablename__ = "creditcards"

    id = db.Column(db.Integer, primary_key=True)
    holder = db.Column(db.String, nullable=False)
    number = db.Column(db.String, nullable=False)
    exp_date = db.Column(db.Date, nullable=False)
    cvv = db.Column(db.String)
    brand = db.Column(db.String)
    key = db.Column(db.String)

    def __init__(self, holder, number, exp_date, cvv=None):
        cipher = AESCipher()
        self.holder = holder
        self.number = cipher.encrypt("".join(filter(str.isdigit, number)))
        self.exp_date = self.get_exp_date(exp_date)
        self.cvv = cvv
        self.brand = self.get_brand(number)
        self.key = cipher.get_key()

    def decrypt_number(self) -> str:
        """
        This method is used to decrypt the credit card number.

        Returns
        -------
        str
            The decrypted credit card number.
        """
        cipher = AESCipher(key=self.key)
        return cipher.decrypt(self.number)

    @staticmethod
    def get_brand(number) -> str:
        """
        This method is used to get the brand of the credit card.

        Parameters
        ----------
        number : str
            The credit card number.

        Returns
        -------
        str
            The brand of the credit card.
        """
        cc = CreditCardValidator(number)
        return cc.get_brand()

    @staticmethod
    def get_exp_date(exp_date) -> datetime.date:
        """
        This method is used to convert the expiration date of the credit card
        to a datetime object.

        Parameters
        ----------
        exp_date : str
            The expiration date of the credit card.

        Returns
        -------
        datetime.date
            The expiration date of the credit card as a datetime object.
        """
        month, year = map(int, exp_date.split("/"))
        _, day = monthrange(year, month)
        exp_dt = datetime(year, month, day)
        return exp_dt.date()

    def serialize(self) -> dict:
        """
        This method is used to serialize the credit card object.

        Returns
        -------
        dict
            The serialized credit card object.
        """
        return {
            "id": self.id,
            "holder": self.holder,
            "number": self.number,
            "exp_date": self.exp_date.strftime("%m/%Y"),
            "cvv": self.cvv,
            "brand": self.brand,
        }
