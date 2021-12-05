from passlib import context
from pydantic import validate_arguments

pwd_context = context.CryptContext(schemes=["bcrypt"], deprecated="auto")


@validate_arguments
def password_hasher(plain_password: str) -> str:
    """Function password_hasher is intented to be used to
    hash passwords before adding data within the
    database

    Args:
        plain_password (str): Password to be hashed

    Returns:
        str: Hashed password
    """
    return pwd_context.hash(plain_password)


@validate_arguments
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Function verify_password is intented to be used to
    verify that a plain password passed and a hashed password
    stored within the database match

    Args:
        plain_password (str): Passed password to be compared
        hashed_password (str): Password within the database
        to be compared

    Returns:
        bool: If the passwords match
    """
    return pwd_context.verify(plain_password, hashed_password)
