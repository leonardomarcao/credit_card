from card_vault.extensions import db
from card_vault.models import CreditCard
from card_vault.utils import AESCipher


class CreditCardDal:
    @staticmethod
    def get_all():
        cards = CreditCard.query.all()
        return [card.serialize() for card in cards]

    @staticmethod
    def get_by_id(id):
        card = CreditCard.query.get(id)
        if not card:
            return {"error": "Card not found"}
        return card.serialize()

    @staticmethod
    def get_by_number(number):
        cards = CreditCard.query.all()

        for card in cards:
            # decrypt each card number
            cipher = AESCipher(key=card.key)
            decrypted_number = cipher.decrypt(card.number)

            # compare decrypted number with the incoming number
            if decrypted_number == number:
                return card.serialize()

        return {"error": "Card not found"}

    @staticmethod
    def create(data):
        card = CreditCard(
            holder=data.holder,
            number=data.number,
            exp_date=data.exp_date,
            cvv=data.cvv,
        )
        db.session.add(card)
        db.session.commit()
        return card.serialize()

    @staticmethod
    def update(id, data):
        card = CreditCard.query.get(id)
        if not card:
            return {"error": "Card not found"}
        card.holder = data.holder
        card.number = data.number
        card.exp_date = data.exp_date
        card.cvv = data.cvv
        db.session.commit()
        return card.serialize()

    @staticmethod
    def delete(id):
        card = CreditCard.query.get(id)
        if not card:
            return {"error": "Card not found"}
        db.session.delete(card)
        db.session.commit()
        return card.serialize()
