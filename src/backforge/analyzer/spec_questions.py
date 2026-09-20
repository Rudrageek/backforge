def generate_specification_questions(
    specification,
) -> list[dict]:
    """
    Generate configuration questions from
    an incomplete BackendSpecification.
    """

    questions = []

    authentication = (
        specification.authentication
    )

    if (
        authentication.get("enabled")
        and authentication.get("method") is None
    ):
        questions.append(
            {
                "id": "authentication_method",
                "category": "authentication",
                "question": (
                    "How should users authenticate?"
                ),
                "type": "single_choice",
                "options": [
                    "email_password",
                    "google",
                    "phone_otp",
                    "magic_link",
                ],
                "required": True,
            }
        )

    database = (
        specification.database
    )

    if (
        database.get("detected")
        and database.get("status")
        == "configuration_required"
    ):
        questions.append(
            {
                "id": "database_provider",
                "category": "database",
                "question": (
                    "Which database should "
                    "the backend use?"
                ),
                "type": "single_choice",
                "options": [
                    "postgresql",
                    "mysql",
                    "mongodb",
                    "supabase",
                ],
                "required": True,
            }
        )

    return questions