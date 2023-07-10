from typing import Union

from flask_restx import ValidationError

from card_vault.api.validators import CreditCardModel
from card_vault.extensions import db
from card_vault.models import CreditCard


class CreditCardDal:
    """
    This class is used to handle the data access layer for the credit card model.

    Methods
    -------
    get_all()
        This method is used to get all credit cards.
    get_by_id(id)
        This method is used to get a credit card by its id.
    get_by_number(number)
        This method is used to get a credit card by its number.
    create(data)
        This method is used to create a credit card.
    update(id, data)
        This method is used to update a credit card.
    delete(id)
        This method is used to delete a credit card.
    """

    @staticmethod
    def get_all() -> list[dict]:
        """
        This method is used to get all credit cards.

        Returns
        -------
        list
            A list of credit cards.
        """
        cards = CreditCard.query.all()
        return [card.serialize() for card in cards]

    @staticmethod
    def get_by_id(id: int) -> Union[dict, None]:
        """
        This method is used to get a credit card by its id.

        Parameters
        ----------
        id : int
            The id of the credit card.

        Returns
        -------
        dict
            The credit card object.
        None
            If the credit card does not exist.
        """
        card = CreditCard.query.get(id)
        if not card:
            return None
        return card.serialize()

    @staticmethod
    def get_by_number(number: str) -> Union[dict, None]:
        """
        This method is used to get a credit card by its number.

        Parameters
        ----------
        number : str
            The number of the credit card.

        Returns
        -------
        dict
            The credit card object.
        None
            If the credit card does not exist.
        """
        number = "".join(filter(str.isdigit, number))
        cards = CreditCard.query.all()

        for card in cards:
            if card.decrypt_number() == number:
                return card.serialize()

        return None

    @staticmethod
    def create(data: CreditCardModel) -> dict:
        """
        This method is used to create a credit card.

        Parameters
        ----------
        data : CreditCardModel
            The credit card data.

        Returns
        -------
        dict
            The credit card object.
        """
        card = CreditCard(
            holder=data.holder,
            number=data.number,
            exp_date=data.exp_date,
            cvv=data.cvv,
        )
        # Check if the credit card already exist before adding it to the database.
        if CreditCardDal.get_by_number(card.decrypt_number()):
            raise ValidationError("Credit card already exists.")
        db.session.add(card)
        db.session.commit()
        return card.serialize()

    @staticmethod
    def update(id: int, data: CreditCardModel) -> Union[dict, None]:
        """
        This method is used to update a credit card.

        Parameters
        ----------
        id : int
            The id of the credit card.
        data : CreditCardModel
            The credit card data.

        Returns
        -------
        dict
            The credit card object.
        None
            If the credit card does not exist.
        """
        card = CreditCard.query.get(id)
        if not card:
            return None
        card.holder = data.holder
        card.number = data.number
        card.exp_date = data.exp_date
        card.cvv = data.cvv
        db.session.commit()
        return card.serialize()

    @staticmethod
    def delete(id: int) -> Union[dict, None]:
        """
        This method is used to delete a credit card.

        Parameters
        ----------
        id : int
            The id of the credit card.

        Returns
        -------
        dict
            The credit card object.
        None
            If the credit card does not exist.
        """
        card = CreditCard.query.get(id)
        if not card:
            return None
        db.session.delete(card)
        db.session.commit()
        return card.serialize()
