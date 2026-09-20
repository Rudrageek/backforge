def generate_user_entity() -> dict:
    return {
        "name": "User",
        "confidence": "high",
        "source": {
            "type": "authentication",
            "method": "email_password",
        },
        "fields": [
            {
                "name": "email",
                "type": "string",
                "unique": True,
            },
            {
                "name": "passwordHash",
                "type": "string",
            },
        ],
    }