from card_vault.models import CreditCard
from card_vault.extensions import db
from datetime import datetime


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
    def create(data):
        card = CreditCard(
            holder=data.holder,
            number=data.number,
            exp_date=datetime.strptime(data.exp_date, "%m/%Y"),
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
        card.exp_date = datetime.strptime(data.exp_date, "%m/%Y")
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
