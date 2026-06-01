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


# GROUP 3: CORE AGENT ORCHESTRATION LAYER - CONTEXT

 # This model acts as the primary unified state container mapping all telemetry,
 # metadata logs, database entities, and token traces into a structured pipeline.

class StructuredDraftContext(BaseModel):
    version: int = 2
    ticket: dict[str, Any] | None = None
    customer: dict[str, Any] | None = None
    signals: DraftSignals | dict[str, Any] | None = None
    highlights: DraftHighlights | dict[str, Any] | None = None
    memory_hits: list[dict[str, Any]] = Field(default_factory=list)
    knowledge_hits: list[dict[str, Any]] = Field(default_factory=list)
    tool_calls: list[DraftToolCall | dict[str, Any]] = Field(default_factory=list)
    errors: list[str] = Field(default_factory=list)


# This model sets the final layout for what the AI draft response sends back.
# It delivers the written email text and packs all the background logs 
# together so the frontend screen can display everything to the agent.

class DraftResponse(BaseModel):
    id: int
    ticket_id: int
    content: str
    context_used: StructuredDraftContext | dict[str, Any] | None = None
    status: str
    created_at: str 

# This model handles changes made by a human supervisor on the dashboard.
# It lets the human edit the email text or change the approval status.

class DraftUpdateRequest(BaseModel):
    content: str | None = None
    status: Literal["pending", "accepted", "discarded"] | None = None

# This model acts like a final packaging box. It bundles the ticket ID 
# and the actual AI-written response together to send it to the frontend.

class GenerateDraftResponse(BaseModel):
    ticket_id: int
    draft: DraftResponse


# GROUP 4: RAG KNOWLEDGE BASE - DATA WIPEOUT CHECKPOINT

# This model controls if we want to delete old policy files from ChromaDB 
# before uploading and indexing the new document checklist folders.

class KnowledgeIngestRequest(BaseModel):
    clear_existing: bool = False

# This model acts as a receipt. After uploading new policy PDFs into 
# ChromaDB, it counts and shows how many files and chunks were indexed.

class KnowledgeIngestResponse(BaseModel):
    files_indexed: int
    chunks_indexed: int
    collection_count: int

# LANGMEM STORAGE - CUSTOMER LONG-TERM MEMORY CONTRACT

class CustomerMemoriesResponse(BaseModel):
    customer_id: int
    customer_email: EmailStr
    memories: list[dict[str, Any]]

# CUSTOMER MEMORY SEARCH RESULT

class CustomerMemorySearchResponse(BaseModel):
    customer_id: int
    customer_email: EmailStr
    query: str
    results: list[dict[str, Any]] 

