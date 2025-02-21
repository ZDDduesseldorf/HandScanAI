import uuid


def generate_uuid() -> str:
    """
    Generates a uuid.

    Returns:
        uuid (str): generated uuid as string
    """
    return str(uuid.uuid4())
