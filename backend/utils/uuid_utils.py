import uuid


def generate_uuid() -> str:
    """
    Function to generate uuid.

    Returns:
        str: generated uuid as string
    """
    return str(uuid.uuid4())
