def generate_questions(
    requirements: dict,
) -> list[dict]:
    """
    Generate configuration questions from
    detected backend requirements.
    """

    questions = []

    authentication = requirements.get(
        "authentication",
        {},
    )

    if (
        authentication.get("detected")
        and authentication.get("status")
        == "configuration_required"
    ):
        questions.append(
            {
                "id": "authentication_method",
                "category": "authentication",
                "question": (
                    "How should users "
                    "authenticate?"
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

    return questions