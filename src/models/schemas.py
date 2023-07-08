from __future__ import annotations

from .typedefs import *

LeadSource = Literal[
    "website",
    "email",
    "phone",
    "chat",
    "facebook",
    "twitter",
    "linkedin",
    "instagram",
    "youtube",
    "whatsapp",
    "other",
]
LeadStatus = Literal[
    "new", "contacted", "qualified", "unqualified", "converted", "rejected", "other"
]
ProductType = Literal["service", "product", "subscription", "other"]
PaymentMethod = Literal["cash", "card", "bank", "paypal", "stripe", "other"]
DealStatus = Literal["proposal", "negotiation", "won", "lost", "other"]


class User(FaunaModel):
    """
    Auth0 User, Github User or Cognito User
    """

    email: Optional[str] = Field(default=None, index=True)
    email_verified: Optional[bool] = Field(default=False)
    family_name: Optional[str] = Field(default=None)
    given_name: Optional[str] = Field(default=None)
    locale: Optional[str] = Field(default=None, index=True)
    name: str = Field(...)
    nickname: Optional[str] = Field(default=None)
    picture: Optional[str] = Field(default=None)
    sub: str = Field(..., unique=True)
    updated_at: Optional[str] = Field(default=None)

class PreviousMessage(BaseModel):
    """
    Pinecone Vector
    """
    text:str = Field(...)
    score:float = Field(...)

class ContextTemplate(BaseModel):
    """
    Context to inject into chatbot context window using Jinja2
    """
    name:str = Field(...)
    role:str = Field(...)
    namespace:str = Field(...)
    context:List[Item] = Field(...)
    previous_messages:Optional[List[PreviousMessage]] = Field(default=None)
    
class Chatbot(FaunaModel):
    org_id: str = Field(..., unique=True)
    template: ContextTemplate = Field(...)

class Message(FaunaModel):
    user_message: str = Field(...)
    ai_message: str = Field(...)
    system_message: str = Field(...)
    tokens: int = Field(...)
    namespace: str = Field(default="default")
    
class Organization(FaunaModel):
    owner:User = Field(...)
    name: str = Field(..., index=True)
    description: str = Field(...)
    members: List[User] = Field(default_factory=list)
    chatbots: List[Chatbot] = Field(default_factory=list)
    
class Upload(FaunaModel):
    user: str = Field(..., description="User sub", index=True)
    name: str = Field(..., description="File name")
    key: str = Field(..., description="File key", unique=True)
    size: int = Field(..., description="File size", gt=0)
    type: str = Field(..., description="File type", index=True)
    lastModified: float = Field(
        default_factory=lambda: datetime.now().timestamp(),
        description="Last modified",
        index=True,
    )
    url: Optional[str] = Field(None, description="File url")


class Lead(FaunaModel):
    email: Optional[str] = Field(default=None)
    name: Optional[str] = Field(default=None)
    source: LeadSource = Field(default="website")
    status: LeadStatus = Field(default="new")
    lead_id: str = Field(..., unique=True)
    ipaddr : str = Field(..., index=True)
    last_seen: float = Field(..., index=True)
    geo_data: Optional[dict] = Field(default=None)



    