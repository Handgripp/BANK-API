create_account_schema = {
    "type": "object",
    "properties": {
        "account_type": {"type": "string", "enum": ["personal", "savings"]},
        "currency": {"type": "string", "enum": ["PLN", "EUR", "GBP", "CHF", "USD"]},
    },
    "required": ["account_type", "currency"]
}