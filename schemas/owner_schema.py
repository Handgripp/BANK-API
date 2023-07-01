create_owner_schema = {
    "type": "object",
    "properties": {
        "first_name": {"type": "string"},
        "last_name": {"type": "string"},
        "email": {"type": "string", "format": "email", "pattern": "^\\S+@\\S+\\.\\S+$"},
        "password": {"type": "string"}
    },
    "required": ["first_name", "last_name", "email", "password"]
}