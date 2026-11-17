from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from authx import TokenPayload
from security import security
from dao.dbuser import DBUser
from logic.project import get_project
from logic.task import get_tasks, add_task, get_task, delete_task, update_task
from logic.timer import start, pause, stop
from dao.dbtimelog import DBTimelog
import os
import datetime

router = APIRouter(tags=["task"])

templates = Jinja2Templates(directory=os.path.join(os.path.dirname("main.py"), "templates"))

@router.get("/tasks/{login}/{project_name}", response_class=HTMLResponse)
async def tasks_g(request: Request, login: str, project_name: str, data: TokenPayload=Depends(security.access_token_required)):
    if login != data.sub: raise HTTPException(status_code=403, detail="No access")
    user = await DBUser.get_user_by_login(login)
    if not user: raise HTTPException(status_code=403, detail="No access")
    project_f = await get_project(user[1], project_name)
    if type(project_f) != dict:
        tasks = await get_tasks(user[1], project_f[1])
        return templates.TemplateResponse(name="tasks.html", request=request, context={"login": user[1],
        "project_name": project_f[1], "tasks": tasks})
    else: raise HTTPException(status_code=404, detail="Not found")

@router.get("/add_task/{login}/{project_name}", response_class=HTMLResponse)
async def add_task_g(request: Request, login: str, project_name: str, data: TokenPayload=Depends(security.access_token_required)):
    if login != data.sub: raise HTTPException(status_code=403, detail="No access")
    user = await DBUser.get_user_by_login(login)
    if not user: raise HTTPException(status_code=403, detail="No access")
    project_f = await get_project(user[1], project_name)
    if type(project_f) != dict:
        csrf_token = request.cookies.get("csrf_access_token")
        return templates.TemplateResponse(name="add_task.html", request=request, context={"login": user[1],
        "project_name": project_f[1], "csrf_token": csrf_token})
    else: raise HTTPException(status_code=404, detail="Not found")

@router.post("/add_task/{login}/{project_name}", response_class=HTMLResponse)
async def add_task_p(request: Request, login: str, project_name: str, data: TokenPayload=Depends(security.access_token_required)):
    if login != data.sub: raise HTTPException(status_code=403, detail="No access")
    user = await DBUser.get_user_by_login(login)
    if not user: raise HTTPException(status_code=403, detail="No access")
    project_f = await get_project(user[1], project_name)
    if type(project_f) != dict:
        form = await request.form()
        name = form.get("name")
        created_at = form.get("created_at")
        description = form.get("description")
        datetime_start = form.get("datetime_start")
        datetime_end = form.get("datetime_end")
        add_task_f = await add_task(user[1], project_f[1], name, created_at, description, datetime_start, datetime_end)
        if add_task_f:
            return RedirectResponse(url=f"/tasks/{user[1]}/{project_f[1]}", status_code=303)
        else:
            return RedirectResponse(url=f"/add_task/{user[1]}/{project_f[1]}", status_code=303)
    else: raise HTTPException(status_code=404, detail="Not found")

@router.get("/task/{login}/{project_name}/{task_name}", response_class=HTMLResponse)
async def task_g(request: Request, login: str, project_name: str, task_name: str, data: TokenPayload=Depends(security.access_token_required)):
    if login != data.sub: raise HTTPException(status_code=403, detail="No access")
    user = await DBUser.get_user_by_login(login)
    if not user: raise HTTPException(status_code=403, detail="No access")
    project_f = await get_project(user[1], project_name)
    if type(project_f) != dict:
        task_f = await get_task(user[1], project_f[1], task_name)
        if type(task_f) != dict and task_f != None:
            csrf_token = request.cookies.get("csrf_access_token")
            time_logs = await DBTimelog.get_time_logs_by_task_id(task_f[0])

            sum_time_logs = 0
            datetime_start = None
            datetime_end = None
            if time_logs:
                datetime_start = time_logs[0][1]
                if task_f[3] == "stop":
                    datetime_end = time_logs[-1][2]

            return templates.TemplateResponse(name="task.html", request=request, context={"login": user[1],
            "project_name": project_f[1], "task_name": task_f[1], "name": task_f[1], "description": task_f[2] if task_f[2] != None else "", "status": task_f[3],
            "created_at": task_f[4], "duration": sum_time_logs, "datetime_start": datetime_start, "datetime_end": datetime_end, "csrf_token": csrf_token})
        else: raise HTTPException(status_code=404, detail="Not found")
    else: raise HTTPException(status_code=404, detail="Not found")

@router.post("/delete_task/{login}/{project_name}/{task_name}")
async def task_p(login: str, project_name: str, task_name: str, data: TokenPayload=Depends(security.access_token_required)):
    if login != data.sub: raise HTTPException(status_code=403, detail="No access")
    user = await DBUser.get_user_by_login(login)
    if not user: raise HTTPException(status_code=403, detail="No access")
    project_f = await get_project(user[1], project_name)
    if type(project_f) != dict:
        task_f = await get_task(user[1], project_f[1], task_name)
        if type(task_f) != dict and task_f != None:
            await delete_task(user[1], project_f[1], task_f[1])
            return RedirectResponse(url=f"/tasks/{user[1]}/{project_f[1]}", status_code=303)
        else: raise HTTPException(status_code=404, detail="Not found")
    else: raise HTTPException(status_code=404, detail="Not found")

@router.get("/update_task/{login}/{project_name}/{task_name}", response_class=HTMLResponse)
async def update_task_g(request: Request, login: str, project_name: str, task_name: str, data: TokenPayload=Depends(security.access_token_required)):
    if login != data.sub: raise HTTPException(status_code=403, detail="No access")
    user = await DBUser.get_user_by_login(login)
    if not user: raise HTTPException(status_code=403, detail="No access")
    project_f = await get_project(user[1], project_name)
    if type(project_f) != dict:
        task_f = await get_task(user[1], project_f[1], task_name)
        if type(task_f) != dict and task_f != None:
            csrf_token = request.cookies.get("csrf_access_token")

            time_logs = await DBTimelog.get_time_logs_by_task_id(task_f[0])

            datetime_start = None
            datetime_end = None
            if time_logs:
                datetime_start = time_logs[0][1]
                if task_f[3] == "stop":
                    datetime_end = time_logs[-1][2]

            return templates.TemplateResponse(name="update_task.html", request=request, context={"login": user[1],
            "project_name": project_f[1], "task_name": task_f[1], "name": task_f[1], "description": task_f[2] if task_f[2] != None else "",
            "created_at": task_f[4], "datetime_start": datetime_start, "datetime_end": datetime_end, "csrf_token": csrf_token})
        else: raise HTTPException(status_code=404, detail="Not found")
    else: raise HTTPException(status_code=404, detail="Not found")

@router.post("/update_task/{login}/{project_name}/{task_name}")
async def update_task_p(request: Request, login: str, project_name: str, task_name: str, data: TokenPayload=Depends(security.access_token_required)):
    if login != data.sub: raise HTTPException(status_code=403, detail="No access")
    user = await DBUser.get_user_by_login(login)
    if not user: raise HTTPException(status_code=403, detail="No access")
    project_f = await get_project(user[1], project_name)
    if type(project_f) != dict:
        task_f = await get_task(user[1], project_f[1], task_name)
        if type(task_f) != dict and task_f != None:
            form = await request.form()
            name = form.get("name")
            created_at = form.get("created_at")
            description = form.get("description")
            datetime_start = form.get("datetime_start")
            datetime_end = form.get("datetime_end")
            update_task_f = await update_task(user[1], project_f[1], task_f[1], name, created_at, description, datetime_start, datetime_end)
            if update_task_f == True:
                return RedirectResponse(url=f"/task/{user[1]}/{project_f[1]}/{name}", status_code=303)
            else: return RedirectResponse(url=f"/update_task/{user[1]}/{project_f[1]}/{task_f[1]}", status_code=303)
        else: raise HTTPException(status_code=404, detail="Not found")
    else:
        raise HTTPException(status_code=404, detail="Not found")

@router.post("/timer/{login}/{project_name}/{task_name}")
async def timer_p(request: Request, login: str, project_name: str, task_name: str, data: TokenPayload=Depends(security.access_token_required)):
    if login != data.sub: raise HTTPException(status_code=403, detail="No access")
    user = await DBUser.get_user_by_login(data.sub)
    if not user: return HTTPException(status_code=403, detail="No access")
    project_f = await get_project(user[1], project_name)
    if type(project_f) != dict:
        task_f = await get_task(user[1], project_f[1], task_name)
        if type(task_f) != dict and task_f != None:
            form = await request.form()
            start_f = form.get("start")
            pause_f = form.get("pause")
            stop_f = form.get("stop")
            if start_f:
                await start(user[1], project_f[1], task_f[1])
            if pause_f:
                await pause(user[1], project_f[1], task_f[1])
            if stop_f:
                await stop(user[1], project_f[1], task_f[1])
            return RedirectResponse(url=f"/task/{user[1]}/{project_name}/{task_name}", status_code=303)
        else: raise HTTPException(status_code=404, detail="Not found")
    else:
        raise HTTPException(status_code=404, detail="Not found")
