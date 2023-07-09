from models.account_model import Account, db


class AccountRepository:

    @staticmethod
    def create_account(account_number, account_type, currency, owner_id, client_id):
        new_account = Account(account_number=account_number, account_type=account_type, currency=currency,
                              owner_id=owner_id, client_id=client_id)
        db.session.add(new_account)
        db.session.commit()

    @staticmethod
    def get_account_by_id(account_number):
        account = Account.query.get(account_number)
        if not account:
            return None

        account_data = {
            'account_number': account.account_number,
            'owner_id': account.owner_id,
            'client_id': account.client_id,
            'account_type': account.account_type,
            'currency': account.currency,
            'balance': account.balance,
            'status': account.status,
        }

        return account_data

    @staticmethod
    def get_accounts_by_user_id(user_id):
        accounts_owner = Account.query.filter_by(owner_id=user_id).all()
        accounts_client = Account.query.filter_by(client_id=user_id).all()
        account_data = []
        for account in accounts_client:
            account_data.append({
                'account_number': account.account_number,
                'owner_id': account.owner_id,
                'client_id': account.client_id,
                'account_type': account.account_type,
                'currency': account.currency,
                'balance': account.balance,
                'status': account.status,
            })
        for account in accounts_owner:
            account_data.append({
                'account_number': account.account_number,
                'owner_id': account.owner_id,
                'client_id': account.client_id,
                'account_type': account.account_type,
                'currency': account.currency,
                'balance': account.balance,
                'status': account.status,
            })

        return account_data

    @staticmethod
    def soft_delete(account_number):
        account = Account.query.filter_by(account_number=account_number).first()
        account.status = "Deleted"
        db.session.commit()

    @staticmethod
    def hard_delete(account_number):
        account = Account.query.filter_by(account_number=account_number).first()
        db.session.delete(account)
        db.session.commit()
