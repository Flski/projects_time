from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from authx import TokenPayload
import os
from security import security
from logic import user
from dao.dbuser import DBUser

router = APIRouter(tags=["profile"])

templates = Jinja2Templates(directory=os.path.join(os.path.dirname("main.py"), "templates"))

@router.get("/profile/{login}", response_class=HTMLResponse)
async def profile_g(request: Request, login: str, data: TokenPayload=Depends(security.access_token_required)):
    user = await DBUser.get_user_by_login(login)
    if user[1] != data.sub: raise HTTPException(status_code=403, detail="No access")
    return templates.TemplateResponse(name="profile.html", request=request, context={"login": user[1]})

@router.get("/exit/{login}")
async def exit_g(login: str, data: TokenPayload=Depends(security.access_token_required)):
    user = await DBUser.get_user_by_login(login)
    if user[1] != data.sub: raise HTTPException(status_code=403, detail="No access")
    response = RedirectResponse(url="/login", status_code=303)
    security.unset_access_cookies(response)
    return response

