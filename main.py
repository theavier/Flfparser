from fastapi import FastAPI, Response, Query
from backbone import get_pages, url
from back_rss import create_rss
#from typing import List
from typing import Annotated


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Rss getter"}

# hur får jag in en eller flera params som
# &adventureTypes=Friluftskunskap&adventureTypes=Allemansrätt&adventureTypes=Djur%20och%20natur&adventureTypes=Första%20hjälpen&adventureTypes=Kris%20och%20säkerhet&adventureTypes=Ledarskap&adventureTypes=Meteorologi&adventureTypes=Navigation
@app.get("/get")
def query(county: str = "Västra%20Götalands%20län", adventuretype: Annotated[list[str] | None, Query()] = None):
    all_adventures = "&".join([f'adventuretype={i}' for i in adventuretype])
    new_url = url.replace('#county#', county).replace('#adventuretype#', all_adventures)    
    #print(f'url {new_url}')
    results = get_pages(new_url)
    rss = create_rss(results, title="Friluftsfrämjandet VGL RSS", desc="Vandringar")
    return Response(content=rss, media_type="application/xml")

@app.get("/generate")
def gen() -> Response:
    # get county strings
    # get adventure type
    return {"message" : "generate"}

# to test api run
# uvicorn main:app --reload