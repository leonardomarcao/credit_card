import json

from .factories import CreditCardFactory


class TestViews:
    def test_get_all_cards(self, testapp, db):
        """
        Tests if all cards are retrieved correctly.
        """
        CreditCardFactory.create()
        db.session.commit()

        response = testapp.get("/api/v1/credit-card")
        data = json.loads(response.body)

        assert response.status_int == 200
        assert len(data) == 1

    def test_get_card_by_number(self, testapp, db):
        """
        Tests if a specific card can be retrieved by its number.
        """
        CreditCardFactory.create()
        db.session.commit()

        response = testapp.get(f"/api/v1/credit-card/{CreditCardFactory.number}")
        data = json.loads(response.body)

        assert response.status_int == 200
        assert data["holder"] == "John Doe"

    def test_create_card(self, testapp, payload):
        """
        Tests if a new card can be created.
        """
        response = testapp.post(
            "/api/v1/credit-card",
            params=json.dumps(payload),
            headers={"Content-Type": "application/json"},
        )
        data = json.loads(response.body)

        assert response.status_int == 201
        assert data["holder"] == "John Doe"

    def test_update_card(self, testapp, db, payload):
        """
        Tests if an existing card can be updated.
        """
        CreditCardFactory.create()
        db.session.commit()

        response = testapp.put(
            f'/api/v1/credit-card/{payload.get("number")}',
            params=json.dumps(payload),
            headers={"Content-Type": "application/json"},
        )
        data = json.loads(response.body)

        assert response.status_int == 200
        assert data["holder"] == "John Doe"

    def test_delete_card(self, testapp, db, payload):
        """
        Tests if an existing card can be deleted.
        """
        CreditCardFactory.create()
        db.session.commit()

        response = testapp.delete(f'/api/v1/credit-card/{payload.get("number")}')

        assert response.status_int == 204
