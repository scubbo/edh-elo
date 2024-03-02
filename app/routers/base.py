from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse

from ..sql import crud
from ..templates import jinja_templates, _jsonify
from ..sql.database import get_db

html_router = APIRouter(include_in_schema=False, default_response_class=HTMLResponse)


@html_router.get("/")
def main(request: Request, db=Depends(get_db)):
    games = crud.get_games(db=db)
    return jinja_templates.TemplateResponse(
        request, "/main.html", {"games": _jsonify(games)}
    )
