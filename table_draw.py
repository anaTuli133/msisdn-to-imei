from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request, Query
from db import fetch_table
from routes import router

templates = Jinja2Templates(directory="templates") 

# @router.get("/view-table", response_class=HTMLResponse)
# def view_table(request: Request, search: str = Query(None)):
#     cols, rows = fetch_table(search_query=search) 
    
#     return templates.TemplateResponse(
#         request=request, 
#         name="CDR14_IMEI_table.html",
#         context={
#             "request": request,
#             "cols": cols, 
#             "rows": rows,
#             "search_query": search
#         }
#     )