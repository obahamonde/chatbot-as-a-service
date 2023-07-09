from geocoder import ip

from .handlers import *


def bootstrap(app_:AioFauna=app):

    @app.on_event("startup")
    async def startup(_):
        try:
            await FaunaModel.create_all()
        except Exception as e:
            print(e)

    @app.post("/api/auth")
    async def user_info(request:Request):
        try:
            token = request.headers.get("Authorization")
            assert isinstance(token, str)
            token = token.split(" ")[-1]
            user = await auth0.user_info(token)
            assert isinstance(user, User)
            app.logger.info("User logged in: %s", user)
            return Response(
                text=user.json(),
                content_type="application/json",
                status=200
            )
        except AssertionError:
            return HTTPException(text=json.dumps({
                "status":"error",
                "message": "Invalid token"
            }))
        except Exception as e:
            return HTTPException(text=json.dumps({
                "status":"error",
                "message": str(e)
            }))
        
    #@app_.middleware
    async def lead_gen_middleware(request: Request, call_next: Callable) -> Response:
        if request.url.path.startswith("/api"):
            lead_id = request.cookies.get("lead_id", None)
            client = request.remote
            if client is None:
                return await call_next(request)
            geo_data = ip(client).json["raw"]
            now = datetime.now().timestamp()
            if lead_id is None:
                lead_id = uuid4().hex
                response = await call_next(request)
                response.set_cookie("lead_id", lead_id)
            else:
                response = await call_next(request)

            lead = Lead(lead_id=lead_id, ipddr=client, geo_data=geo_data, last_seen=now)
            await lead.save()
            return response
        
        return await call_next(request)
    
    return app_