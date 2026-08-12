from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime






class UserModel(BaseModel):
    name: str = Field(..., example="Juan Pérez")
    email: EmailStr = Field(..., example="juan@empresa.com")
    area: str = Field(..., example="Sistemas")  
    role: str = Field(default="user", example="user")  
    face_encoding: Optional[List[float]] = None  
    created_at: datetime = Field(default_factory=datetime.utcnow)



class UserUpdateModel(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    area: Optional[str] = None
    role: Optional[str] = None
    face_encoding: Optional[List[float]] = None









class AttendanceModel(BaseModel):
    user_id: str = Field(..., example="64d1f2b3e4b0a123456789ab")
    name: str = Field(..., example="Juan Pérez")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    status: str = Field(default="EXITOSO", example="EXITOSO")  