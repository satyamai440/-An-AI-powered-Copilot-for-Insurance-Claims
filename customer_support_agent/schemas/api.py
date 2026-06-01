from __future__ import annotations
from typing import Any,Literal
from pydantic import BaseModel,EmailStr,Field

## Group 1: External Client & Claim Intake Layer

# Ticket Creation Request — Input Validation Schema
class TicketCreateRequest(BaseModel):
    customer_email: EmailStr
    customer_name: str | None = None 
    customer_company: str | None = None
    subject: str = Field(min_length=3)
    description: str = Field(min_length=10)
    priority: Literal["low", "medium", "high", "urgent"] = "medium"
    auto_generate: bool = True

# Ticket Response Schema — What the API Sends Back After a Ticket is Created:

class TicketResponse(BaseModel):
    id: int
    customer_id: int
    customer_email: EmailStr
    customer_name: str | None = None
    customer_company: str | None = None
    subject: str
    description: str
    status: str
    priority: str
    created_at: str
    updated_at: str

