from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from authx import TokenPayload
import os
from security import security
from logic.user import update_login, update_password, delete_user
from dao.dbuser import DBUser

router = APIRouter(tags=["profile"])

templates = Jinja2Templates(directory=os.path.join(os.path.dirname("main.py"), "templates"))

@router.get("/profile/{login}", response_class=HTMLResponse)
async def profile_g(request: Request, login: str, data: TokenPayload=Depends(security.access_token_required)):
    user = await DBUser.get_user_by_login(login)
    if user:
        if user[1] != data.sub: raise HTTPException(status_code=403, detail="No access")
    else: raise HTTPException(status_code=403, detail="No access")
    return templates.TemplateResponse(name="profile.html", request=request, context={"login": user[1]})

@router.get("/exit/{login}")
async def exit_g(login: str, data: TokenPayload=Depends(security.access_token_required)):
    user = await DBUser.get_user_by_login(login)
    if user:
        if user[1] != data.sub: raise HTTPException(status_code=403, detail="No access")
    else: raise HTTPException(status_code=403, detail="No access")
    response = RedirectResponse(url="/login", status_code=303)
    security.unset_access_cookies(response)
    return response

@router.get("/update_password/{login}", response_class=HTMLResponse)
async def update_password_g(request: Request, login: str, data: TokenPayload=Depends(security.access_token_required)):
    user = await DBUser.get_user_by_login(login)
    if user:
        if user[1] != data.sub: raise HTTPException(status_code=403, detail="No access")
    else: raise HTTPException(status_code=403, detail="No access")
    csrf_token = request.cookies.get("csrf_access_token")
    return templates.TemplateResponse(name="update_password.html", request=request, context={"login": user[1], "csrf_token": csrf_token})

@router.post("/update_password/{login}")
async def update_password_p(request: Request, login: str, data: TokenPayload=Depends(security.access_token_required)):
    user = await DBUser.get_user_by_login(login)
    if user:
        if user[1] != data.sub: raise HTTPException(status_code=403, detail="No access")
    else: raise HTTPException(status_code=403, detail="No access")
    form = await request.form()
    password = form.get("password")
    password1 = form.get("password1")
    await update_password(user[1], password, password1)
    return RedirectResponse(url=f"/update_password/{user[1]}", status_code=303)

@router.get("/update_login/{login}", response_class=HTMLResponse)
async def update_login_g(request: Request, login: str, data: TokenPayload=Depends(security.access_token_required)):
    user = await DBUser.get_user_by_login(login)
    if user:
        if user[1] != data.sub: raise HTTPException(status_code=403, detail="No access")
    else: raise HTTPException(status_code=403, detail="No access")
    csrf_token = request.cookies.get("csrf_access_token")
    return templates.TemplateResponse(name="update_login.html", request=request, context={"login": user[1], "csrf_token": csrf_token})

@router.post("/update_login/{login}", response_class=HTMLResponse)
async def update_login_p(request: Request, login: str, data: TokenPayload=Depends(security.access_token_required)):
    user = await DBUser.get_user_by_login(login)
    if user:
        if user[1] != data.sub: raise HTTPException(status_code=403, detail="No access")
    else: raise HTTPException(status_code=403, detail="No access")
    form = await request.form()
    password = form.get("password")
    login_ = form.get("login")
    update_login_f = await update_login(user[1], password, login_)
    if update_login_f:
        response = RedirectResponse(url=f"/update_login/{login_.strip()}", status_code=303)
        security.unset_access_cookies(response)
        token = security.create_access_token(uid=login_.strip())
        security.set_access_cookies(token, response)
        return response
    else: return RedirectResponse(url=f"/update_login/{user[1]}", status_code=303)

@router.get("/delete_profile/{login}", response_class=HTMLResponse)
async def delete_profile_g(request: Request, login: str, data: TokenPayload=Depends(security.access_token_required)):
    user = await DBUser.get_user_by_login(login)
    if user:
        if user[1] != data.sub: raise HTTPException(status_code=403, detail="No access")
    else: raise HTTPException(status_code=403, detail="No access")
    csrf_token = request.cookies.get("csrf_access_token")
    return templates.TemplateResponse(name="delete_profile.html", request=request, context={"login": user[1], "csrf_token": csrf_token})

@router.post("/delete_profile/{login}", response_class=HTMLResponse)
async def delete_profile_p(request: Request, login: str, data: TokenPayload=Depends(security.access_token_required)):
    user = await DBUser.get_user_by_login(login)
    if user:
        if user[1] != data.sub: raise HTTPException(status_code=403, detail="No access")
    else: raise HTTPException(status_code=403, detail="No access")
    form = await request.form()
    password = form.get("password")
    delete_profile_f = await delete_user(user[1], password)
    if delete_profile_f:
        response = RedirectResponse(url="/login", status_code=303)
        security.unset_access_cookies(response)
        return response
    return RedirectResponse(url=f"/delete_profile/{user[1]}", status_code=303)
