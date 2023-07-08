from datetime import datetime
from typing import *
from uuid import uuid4

from aiofauna import *
from multidict import CIMultiDict, CIMultiDictProxy, MultiDict, MultiDictProxy

from ..config import env

T = TypeVar("T")
Headers = Union[
    CIMultiDictProxy, CIMultiDict, MultiDictProxy, MultiDict, Dict[str, str]
]
Method = Literal["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS", "TRACE"]
Json = Union[Dict[str, Any], List[Any], str, int, float, bool, None]

Vector = List[float]
Scalar = Union[float, int, str, bool]
Context = Dict[str, str]
Method = Literal["GET", "POST", "PUT", "DELETE", "PATCH"]

class Item(BaseModel):
    key: str = Field(...)
    value: str = Field(...)

class Function(BaseModel):
    name: str = Field(..., alias="FunctionName", index=True)
    runtime: str = Field(default="python3.9", alias="Runtime")
    role: str = Field(env.AWS_LAMBDA_ROLE, alias="Role")
    handler: str = Field("main.handler", alias="Handler")
    code: Item = Field(..., alias="Code")
    timeout: int = Field(default=3, alias="Timeout")
    memory: int = Field(default=128, alias="MemorySize")
    publish: bool = Field(default=True, alias="Publish")
    env: Optional[Dict[str, str]] = Field(default=None, alias="Environment")
    url: Optional[str] = Field(default=None, alias="FunctionUrl")
    arn: Optional[str] = Field(default=None, alias="FunctionArn")