
from extensions import db
from models.account_model import Account
from models.transaction_model import Transaction
from sqlalchemy.orm import sessionmaker


class TransactionRepository:
    @staticmethod
    def transaction(account_number_from, account_number_to, amount, exchange_from, exchange_to):
        Session = sessionmaker(bind=db.engine)
        session = Session()
        account_from = session.query(Account).filter_by(account_number=account_number_from).first()
        account_to = session.query(Account).filter_by(account_number=account_number_to).first()

        if not account_from or not account_to:
            session.close()
            return None

        if account_from.balance < amount:
            session.close()
            return None

        try:

            converted_amount = amount * exchange_from / exchange_to

            account_from.balance -= amount
            account_to.balance += converted_amount

            transaction = Transaction(
                account_number_from=account_number_from,
                account_number_to=account_number_to,
                amount=amount
            )

            session.add(transaction)
            session.commit()
            return transaction
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    @staticmethod
    def deposit(account_number_to, amount):
        Session = sessionmaker(bind=db.engine)
        session = Session()
        account_to = session.query(Account).filter_by(account_number=account_number_to).first()

        if not account_to:
            session.close()
            return None

        try:
            account_to.balance += amount

            transaction = Transaction(
                account_number_to=account_number_to,
                amount=amount
            )

            session.add(transaction)
            session.commit()
            return transaction
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    @staticmethod
    def get_transaction_by_id(transaction_id):
        transaction = Transaction.query.get(transaction_id)
        if not transaction:
            return None

        transaction_data = {
            'id': transaction.id,
            'account_number_from': transaction.account_number_from,
            'account_number_to': transaction.account_number_to,
            'created_at': transaction.created_at,
            'amount': transaction.amount,
            'type': transaction.type,
        }

        return transaction_data

    @staticmethod
    def get_transactions_by_account(account_number_from):
        transactions = Transaction.query.filter_by(account_number_from=account_number_from).all()
        if not transactions:
            return None

        transaction_data = []
        for transaction in transactions:
            transaction_data.append({
                'id': transaction.id,
                'account_number_from': transaction.account_number_from,
                'account_number_to': transaction.account_number_to,
                'created_at': transaction.created_at,
                'amount': transaction.amount,
                'type': transaction.type,
            })

        return transaction_data


