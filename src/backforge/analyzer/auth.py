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


def generate_session_entity() -> dict:
    return {
        "name": "Session",
        "confidence": "high",
        "source": {
            "type": "authentication",
            "method": "email_password",
        },
        "fields": [
            {
                "name": "token",
                "type": "string",
                "unique": True,
            },
            {
                "name": "userId",
                "type": "string",
            },
            {
                "name": "expiresAt",
                "type": "date",
            },
        ],
    }