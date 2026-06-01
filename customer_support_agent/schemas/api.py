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


# GROUP 2: Behind-the-Scenes AI Activity Tracking

# Tracks what the AI agent actually did while generating a response —
# how many times it checked memory, searched the knowledge base, and called external tools.

class DraftSignals(BaseModel):
    memory_hit_count: int = 0
    knowledge_hit_count: int = 0
    tool_call_count: int = 0
    tool_error_count: int = 0
    knowledge_sources: list[str] = Field(default_factory=list)


# This model structures the high-level semantic summaries (memory, RAG, 
# and tool logs) displayed to the human agent for full audit transparency.

class DraftHighlights(BaseModel):
    memory: list[str] = Field(default_factory=list)
    knowledge: list[str] = Field(default_factory=list)
    tools: list[str] = Field(default_factory=list)

# This model captures and validates the dynamic input arguments, status, 
# and schema outputs of autonomous external tool invocations by the AI.

class DraftToolCall(BaseModel):
    tool_name: str
    tool_call_id: str | None = None
    arguments: dict[str, Any] = Field(default_factory=dict)
    status: str
    summary: str | None = None
    output: dict[str, Any] | None = None
    output_text: str


