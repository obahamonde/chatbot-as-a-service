from aiofauna import *
from aiofauna.json import FaunaJSONEncoder

from ..config import env
from ..models import *
from ..tools import *


class AuthClient(ApiClient):
    async def user_info(self, token: str):
        try:
            user_dict = await self.fetch(f"{env.AUTH0_DOMAIN}/userinfo", headers={
                "Authorization": f"Bearer {token}"
            })
            assert isinstance(user_dict, dict)  
            return await User(**user_dict).save()
            
        except (AssertionError, HTTPException) as exc:
            return HTTPException(text=json.dumps({
                "status":"error",
                "message": str(exc)
            }))
            