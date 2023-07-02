create_client_schema = {
    "type": "object",
    "properties": {
        "first_name": {"type": "string"},
        "last_name": {"type": "string"},
        "is_gender_male": {"type": "boolean"},
        "pesel": {"type": "string", "minLength": 11, "maxLength": 11},
        "email": {"type": "string", "format": "email", "pattern": "^\\S+@\\S+\\.\\S+$"},
        "password": {"type": "string"}
    },
    "required": ["first_name", "last_name", "is_gender_male", "pesel", "email", "password"]
}