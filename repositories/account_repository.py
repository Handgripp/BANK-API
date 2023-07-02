from models.account_model import Account, db


class AccountRepository:

    @staticmethod
    def create_account(account_number, account_type, currency, owner_id, client_id):
        new_account = Account(account_number=account_number, account_type=account_type, currency=currency,
                              owner_id=owner_id, client_id=client_id)
        db.session.add(new_account)
        db.session.commit()
