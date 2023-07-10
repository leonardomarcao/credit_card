from flask import Blueprint, abort
from flask_restx import Api, Resource
from pydantic import ValidationError

from card_vault import settings
from card_vault.api.validators import CreditCardModel
from card_vault.dal import CreditCardDal
from card_vault.extensions import auth
from card_vault.settings import AUTHORIZATIONS
from card_vault.utils import pydantic_to_flask_restx, requires_auth

blueprint = Blueprint("api", __name__)
api = Api(blueprint, authorizations=AUTHORIZATIONS, doc="/docs/")

card_fields = api.model("CreditCard", pydantic_to_flask_restx(CreditCardModel))


@auth.verify_password
def verify_password(username, password):
    if (
        username == settings.BASIC_AUTH_USERNAME
        and password == settings.BASIC_AUTH_PASSWORD
    ):
        return username


@api.route("/api/v1/credit-card")
@api.response(403, "Unauthorized access")
class CreditCardListResource(Resource):
    @api.doc("list_cards", security="basicAuth")
    @api.marshal_list_with(card_fields)
    @requires_auth
    def get(self):
        """List all cards"""
        cards = CreditCardDal.get_all()
        return cards

    @api.doc("create_card", security="basicAuth")
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
        except Exception as e:
            abort(400, str(e))


@api.route("/api/v1/credit-card/<string:number>")
@api.response(404, "Card not found")
@api.param("number", "The number of the card to fetch")
class CreditCardResource(Resource):
    @api.doc("get_card", security="basicAuth")
    @api.marshal_with(card_fields)
    def get(self, number):
        """Fetch a card given its number"""
        card = CreditCardDal.get_by_number(number)
        if not card:
            api.abort(404, "Card not found")
        return card

    @api.doc("update_card", security="basicAuth")
    @api.expect(card_fields)
    @api.marshal_with(card_fields)
    def put(self, id):
        """Update a card given its number"""
        try:
            payload = CreditCardModel(**api.payload)
            card = CreditCardDal.update(id, payload)
            if not card:
                api.abort(404, "Card not found")
            return card
        except ValidationError as e:
            abort(400, str(e))

    @api.doc("delete_card", security="basicAuth")
    @api.response(204, "Card deleted")
    def delete(self, id):
        """Delete a card given its number"""
        deleted = CreditCardDal.delete(id)
        if not deleted:
            api.abort(404, "Card not found")
        return None, 204
