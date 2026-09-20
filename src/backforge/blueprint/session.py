from backforge.analyzer.spec_questions import (
    generate_specification_questions,
)

from backforge.blueprint.answers import (
    apply_answer,
)

from backforge.blueprint.specification import (
    BackendSpecification,
)


class ConfigurationSession:
    """
    Manage the process of answering backend
    configuration questions.
    """

    def __init__(
        self,
        specification: BackendSpecification,
    ):
        self.specification = specification

    def get_questions(self) -> list[dict]:
        """
        Return all currently unanswered questions.
        """

        return generate_specification_questions(
            self.specification
        )

    def answer(
        self,
        question_id: str,
        value: str,
    ) -> BackendSpecification:
        """
        Apply an answer to the specification.
        """

        questions = self.get_questions()

        question_ids = {
            question["id"]
            for question in questions
        }

        if question_id not in question_ids:
            raise ValueError(
                f"Unknown or already answered "
                f"question: {question_id}"
            )

        self.specification = apply_answer(
            self.specification,
            question_id,
            value,
        )

        return self.specification

    def is_complete(self) -> bool:
        """
        Check whether all required configuration
        questions have been answered.
        """

        return len(
            self.get_questions()
        ) == 0