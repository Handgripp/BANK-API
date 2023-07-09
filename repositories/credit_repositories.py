from models.credit_model import Credit, db, CreditPayments


class CreditRepository:

    @staticmethod
    def create_credit(client_id, account_number, amount_credit, loan_term, interest_rate):
        new_credit = Credit(client_id=client_id, account_number=account_number, amount_credit=amount_credit,
                            loan_term=loan_term, interest_rate=interest_rate)
        db.session.add(new_credit)
        db.session.commit()

        return new_credit.id

    @staticmethod
    def credit_payments(credit_id, client_id, account_number, payment_date,
                        amount_credit, remaining_installments, loan_payment, is_paid):
        credit = CreditPayments(credit_id=credit_id, client_id=client_id, account_number=account_number,
                                payment_date=payment_date,amount_credit=amount_credit,
                                remaining_installments=remaining_installments, loan_payment=loan_payment,
                                is_paid=is_paid)
        db.session.add(credit)
        db.session.commit()

    @staticmethod
    def get_all_credits():
        return Credit.query.all()