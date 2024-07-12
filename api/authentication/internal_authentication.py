from passlib.context import CryptContext
from sqlmodel import select

from api.models.assessment import Assessment
from api.models.internal_credentials import InternalCredentials

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_user_credentials(session, exam_code: str, username: str):
    query = (
        select(InternalCredentials)
        .join(Assessment)
        .where(
            InternalCredentials.username == username, Assessment.exam_code == exam_code
        )
    )
    return session.exec(query).first()


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
