create_credit_schema = {
    "type": "object",
    "properties": {
        "account_number_client": {"type": "string"},
        "payment_date": {"type": "string", "format": "date"},
        "amount_credit": {"type": "integer"},
        "loan_term": {"type": "integer"},
    },
    "required": ["account_number_client", "amount_credit", "loan_term"]
}