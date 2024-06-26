from fastapi import FastAPI, Response, Query
from backbone import get_pages, set_url_basic
from back_rss import create_rss
from typing import Annotated
from urllib.parse import unquote

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Rss getter"}


@app.get("/get")
def query(county: str = "Västra%20Götalands%20län", adventuretype: Annotated[list[str] | None, Query()] = None):
    """ retrieves adventures
    example http://localhost:7000/get?adventuretype=vandring&adventuretype=ledarskap """
    results = get_pages(set_url_basic(county=county, _at_list=adventuretype))
    rss = create_rss(results, title=f"Friluftsfrämjandet {unquote(county)} RSS", desc=",".join(adventuretype))
    return Response(content=rss, media_type="application/xml")

@app.get("/generate")
def gen() -> Response:
    # get county strings
    # get adventure type
    return {"message" : "generate"}

# to test api run
# uvicorn main:app --reload --port 7000