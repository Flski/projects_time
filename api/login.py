from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import os
from security import security
from logic.login import registration, login

router = APIRouter(tags=["login"])

templates = Jinja2Templates(directory=os.path.join(os.path.dirname("main.py"), "templates"))

@router.get("/")
async def main_g():
    response = RedirectResponse(url="/login", status_code=303)
    security.unset_access_cookies(response)
    return response

@router.get("/login", response_class=HTMLResponse)
async def login_g(request: Request):
    response = templates.TemplateResponse(name="login.html", request=request)
    security.unset_access_cookies(response)
    return response

@router.post("/login")
async def login_p(request: Request):
    form = await request.form()
    login_ = form.get("login")
    password_ = form.get("password")
    login_f = await login(login_, password_)
    if login_f == True:
        response = RedirectResponse(url=f"/profile/{login_.strip()}", status_code=303)
        token = security.create_access_token(uid=login_.strip())
        security.unset_access_cookies(response)
        security.set_access_cookies(token, response)
        return response
    else:
        response = RedirectResponse(url="/login", status_code=303)
        security.unset_access_cookies(response)
        return response

@router.get("/registration", response_class=HTMLResponse)
async def registration_g(request: Request):
    response = templates.TemplateResponse(name="registration.html", request=request)
    security.unset_access_cookies(response)
    return response

@router.post("/registration")
async def registration_p(request: Request):
    form = await request.form()
    login_ = form.get("login")
    password_ = form.get("password")
    password1_ = form.get("password1")
    registration_f = await registration(login_, password_, password1_)
    if registration_f == True:
        response = RedirectResponse(url="/login",  status_code=303)
    else:
        response = RedirectResponse(url="/registration", status_code=303)
    security.unset_access_cookies(response)
    return response