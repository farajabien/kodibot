from pydantic import BaseModel
from typing import Optional

class ChatRequest(BaseModel):
    phone_number: str
    message: str

class ChatResponse(BaseModel):
    response: Optional[str] = None
    error: Optional[str] = None
    requires_linking: Optional[bool] = False

class LinkingRequest(BaseModel):
    phone_number: str
    citizen_id: str

class OTPVerificationRequest(BaseModel):
    phone_number: str
    otp_code: str

class LinkingResponse(BaseModel):
    success: bool
    message: str
    otp: Optional[str] = None