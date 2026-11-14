from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from authx import TokenPayload
import os
from security import security
from logic.project import get_projects
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