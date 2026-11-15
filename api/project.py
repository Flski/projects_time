from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from authx import TokenPayload
import os
from security import security
from logic.project import get_projects, add_project, get_project, delete_project, update_project
from dao.dbuser import DBUser

router = APIRouter(tags=["project"])

templates = Jinja2Templates(directory=os.path.join(os.path.dirname("main.py"), "templates"))

@router.get("/projects/{login}", response_class=HTMLResponse)
async def projects_g(request: Request, login: str, data: TokenPayload=Depends(security.access_token_required)):
    if login != data.sub: raise HTTPException(status_code=403, detail="No access")
    user = await DBUser.get_user_by_login(data.sub)
    if not user: raise HTTPException(status_code=403, detail="No access")
    projects = await get_projects(user[1])
    return templates.TemplateResponse(name="projects.html", request=request, context={"login": user[1],
    "projects": projects})

@router.get("/add_project/{login}", response_class=HTMLResponse)
async def add_project_g(request: Request, login: str, data: TokenPayload=Depends(security.access_token_required)):
    if login != data.sub: raise HTTPException(status_code=403, detail="No access")
    user = await DBUser.get_user_by_login(login)
    if not user: raise HTTPException(status_code=403, detail="No access")
    csrf_token = request.cookies.get("csrf_access_token")
    return templates.TemplateResponse(name="add_project.html", request=request, context={"login": user[1], "csrf_token": csrf_token})

@router.post("/add_project/{login}", response_class=HTMLResponse)
async def add_project_p(request: Request, login: str, data: TokenPayload=Depends(security.access_token_required)):
    if login != data.sub: raise HTTPException(status_code=403, detail="No access")
    user = await DBUser.get_user_by_login(login)
    if not user: raise HTTPException(status_code=403, detail="No access")
    form = await request.form()
    name = form.get("name")
    description = form.get("description")
    created_at = form.get("created_at")
    add_project_f = await add_project(user[1], name, created_at, description)
    if add_project_f == True:
        return RedirectResponse(url=f"/projects/{user[1]}", status_code=303)
    else: return RedirectResponse(url=f"/add_project/{user[1]}", status_code=303)

@router.get("/project/{login}/{project_name}", response_class=HTMLResponse)
async def project_g(request: Request, login: str, project_name: str, data: TokenPayload=Depends(security.access_token_required)):
    if login != data.sub: raise HTTPException(status_code=403, detail="No access")
    user = await DBUser.get_user_by_login(login)
    if not user: raise HTTPException(status_code=403, detail="No access")
    project_f = await get_project(user[1], project_name)
    if type(project_f) != dict:
        csrf_token = request.cookies.get("csrf_access_token")
        return templates.TemplateResponse(name="project.html", request=request, context={"login": user[1], "name": project_f[1],
        "description": project_f[2], "created_at": project_f[3], "project_name": project_f[1], "csrf_token": csrf_token})
    else: raise HTTPException(status_code=404, detail="Not found")

@router.post("/delete_project/{login}/{project_name}", response_class=HTMLResponse)
async def project_p(login: str, project_name: str, data: TokenPayload=Depends(security.access_token_required)):
    if login != data.sub: raise HTTPException(status_code=403, detail="No access")
    user = await DBUser.get_user_by_login(login)
    if not user: raise HTTPException(status_code=403, detail="No access")
    project_f = await get_project(user[1], project_name)
    if type(project_f) != dict:
        await delete_project(user[1], project_f[1])
        return RedirectResponse(url=f"/projects/{user[1]}", status_code=303)
    else: raise HTTPException(status_code=404, detail="Not found")

@router.get("/update_project/{login}/{project_name}", response_class=HTMLResponse)
async def update_project_g(request: Request, login: str, project_name: str, data: TokenPayload=Depends(security.access_token_required)):
    if login != data.sub: raise HTTPException(status_code=403, detail="No access")
    user = await DBUser.get_user_by_login(login)
    if not user: raise HTTPException(status_code=403, detail="No access")
    project_f = await get_project(user[1], project_name)
    if type(project_f) != dict:
        csrf_token = request.cookies.get("csrf_access_token")
        return templates.TemplateResponse(name="update_project.html", request=request, context={"login": user[1], "name": project_f[1],
        "description": project_f[2], "created_at": project_f[3], "project_name": project_f[1], "csrf_token": csrf_token})
    else: raise HTTPException(status_code=404, detail="Not found")

@router.post("/update_project/{login}/{project_name}", response_class=HTMLResponse)
async def update_project_g(request: Request, login: str, project_name: str, data: TokenPayload=Depends(security.access_token_required)):
    if login != data.sub: raise HTTPException(status_code=403, detail="No access")
    user = await DBUser.get_user_by_login(login)
    if not user: raise HTTPException(status_code=403, detail="No access")
    project_f = await get_project(user[1], project_name)
    form = await request.form()
    name = form.get("name")
    created_at = form.get("created_at")
    description = form.get("description")
    if type(project_f) != dict:
        update_project_f = await update_project(user[1], project_f[1], name, created_at, description)
        if update_project_f:
            return RedirectResponse(url=f"/project/{user[1]}/{name.strip()}", status_code=303)
        else: return RedirectResponse(url=f"/update_project/{user[1]}/{project_f[1]}", status_code=303)
    else: raise HTTPException(status_code=404, detail="Not found")

