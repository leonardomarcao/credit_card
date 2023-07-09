from flask import Blueprint, jsonify, request
from flask_restful import Api, Resource
from pydantic import ValidationError

from card_vault.dal import CreditCardDal
from card_vault.api.validators import CreditCardModel

blueprint = Blueprint("api", __name__)
api = Api(blueprint)


class CreditCardListResource(Resource):
    def get(self):
        cards = CreditCardDal.get_all()
        return jsonify(cards)

    def post(self):
        data = request.get_json()
        try:
            validated_data = CreditCardModel(**data)
        except ValidationError as e:
            return jsonify({"errors": e.errors()}), 400

        card = CreditCardDal.create(validated_data)
        return jsonify(card.serialize()), 201


class CreditCardResource(Resource):
    def get(self, id):
        card = CreditCardDal.get_by_id(id)
        if not card:
            return jsonify({"error": "Card not found"}), 404
        return jsonify(card.serialize())


api.add_resource(CreditCardListResource, "/api/v1/credit-card")
api.add_resource(CreditCardResource, "/api/v1/credit-card/<int:id>")
