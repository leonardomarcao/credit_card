from datetime import datetime

from flask import Blueprint, jsonify, request
from flask_restful import Api, Resource
from pydantic import ValidationError

from card_vault.api.models import CreditCard, db
from card_vault.api.validators import CreditCardModel

blueprint = Blueprint("api", __name__)
api = Api(blueprint)


class CreditCardListResource(Resource):
    def get(self):
        cards = CreditCard.query.all()
        return jsonify([card.serialize() for card in cards])

    def post(self):
        data = request.get_json()
        try:
            validated_data = CreditCardModel(**data)
        except ValidationError as e:
            return jsonify({"errors": e.errors()}), 400

        card = CreditCard(
            holder=validated_data.holder,
            number=validated_data.number,
            exp_date=datetime.strptime(validated_data.exp_date, "%m/%Y"),
            cvv=validated_data.cvv,
        )
        db.session.add(card)
        db.session.commit()
        return jsonify(card.serialize()), 201


class CreditCardResource(Resource):
    def get(self, id):
        card = CreditCard.query.get(id)
        if not card:
            return jsonify({"error": "Card not found"}), 404
        return jsonify(card.serialize())


api.add_resource(CreditCardListResource, "/api/v1/credit-card")
api.add_resource(CreditCardResource, "/api/v1/credit-card/<int:id>")
