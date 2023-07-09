from flask import Blueprint, abort
from flask_restx import Api, Resource
from pydantic import ValidationError

from card_vault.api.validators import CreditCardModel
from card_vault.dal import CreditCardDal
from card_vault.utils import pydantic_to_flask_restx

blueprint = Blueprint("api", __name__)
api = Api(blueprint, doc="/docs/")

card_fields = api.model("CreditCard", pydantic_to_flask_restx(CreditCardModel))


@api.route("/api/v1/credit-card")
class CreditCardListResource(Resource):
    @api.doc("list_cards")
    @api.marshal_list_with(card_fields)
    def get(self):
        """List all cards"""
        cards = CreditCardDal.get_all()
        return cards

    @api.doc("create_card")
    @api.expect(card_fields)
    @api.marshal_with(card_fields, code=201)
    def post(self):
        """Create a new card"""
        try:
            payload = CreditCardModel(**api.payload)
            card = CreditCardDal.create(payload)
            return card
        except ValidationError as e:
            abort(400, str(e))


@api.route("/api/v1/credit-card/<int:id>")
@api.response(404, "Card not found")
@api.param("id", "The card identifier")
class CreditCardResource(Resource):
    @api.doc("get_card")
    @api.marshal_with(card_fields)
    def get(self, id):
        """Fetch a card given its identifier"""
        card = CreditCardDal.get_by_id(id)
        if not card:
            api.abort(404, "Card not found")
        return card

    @api.doc("create_card")
    @api.expect(card_fields)
    @api.marshal_with(card_fields, code=201)
    def post(self, payload):
        """Create a new card"""
        payload = api.payload  # Get the request body

        # Validate the payload using the Pydantic model
        try:
            validated_payload = CreditCardModel(**payload)
        except ValidationError as e:
            abort(400, str(e))  # Return a 400 Bad Request error if validation fails

        # If validation passes, create the card
        card = CreditCardDal.create(validated_payload)
        return card, 201

    @api.doc("update_card")
    @api.expect(card_fields)
    @api.marshal_with(card_fields)
    def put(self, id):
        """Update a card given its identifier"""
        try:
            payload = CreditCardModel(**api.payload)
            card = CreditCardDal.update(id, payload)
            if not card:
                api.abort(404, "Card not found")
            return card
        except ValidationError as e:
            abort(400, str(e))

    @api.doc("delete_card")
    @api.response(204, "Card deleted")
    def delete(self, id):
        """Delete a card given its identifier"""
        deleted = CreditCardDal.delete(id)
        if not deleted:
            api.abort(404, "Card not found")
        return None, 204


api.add_resource(CreditCardListResource, "/api/v1/credit-card")
api.add_resource(CreditCardResource, "/api/v1/credit-card/<int:id>")
