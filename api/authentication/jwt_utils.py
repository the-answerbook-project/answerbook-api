from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/{assessment_code}/login")
JWT_ALGO = "HS256"
TWO_HOURS_IN_MINUTES = 120


class JwtSubject(BaseModel):
    username: str
    role: str
    assessment_code: str


class Token(BaseModel):
    access_token: str
    token_type: str
