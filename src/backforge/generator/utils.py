def prisma_delegate_name(model_name: str) -> str:
    """
    Convert a Prisma model name such as
    UserProfile into its client delegate name:
    userProfile.
    """

    if not model_name:
        raise ValueError("Model name cannot be empty.")

    return model_name[0].lower() + model_name[1:]