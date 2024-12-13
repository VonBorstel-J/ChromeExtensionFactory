# /backend/schemas.py (Updated)
from pydantic import BaseModel, EmailStr
from typing import Any, Optional

class UserSignupSchema(BaseModel):
    email: EmailStr
    password: str

class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str

class CodeGenerationSchema(BaseModel):
    user_idea: str
    template_type: str
    provider: Optional[str] = "openai"

class ProjectSchema(BaseModel):
    name: str
    data: Any
