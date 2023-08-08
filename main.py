from fastapi import FastAPI, Response
from backbone import get_pages, url
from back_rss import create_rss

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Rss getter"}

@app.get("/get")
def pong():
    results = get_pages(url)
    rss = create_rss(results, title="Friluftsfrämjandet VGL RSS", desc="Vandringar")
    return Response(content=rss, media_type="application/xml")

# to test api run
# uvicorn main:app --reload