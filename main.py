from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

posts: list[dict] = [
    {
        "id": 1,
        "author": "Aegiris",
        "title": "FIRST BLOG !!!1!",
        "content": "This is the first ever post on this blog made by..... ME :D!",
        "date_posted": "September 19, 2025"        
    },    
    
    {
        "id": 2,
        "author": "Skadi",
        "title": "How do i use fastAPI?",
        "content": "I heard that this framework is really convenient and easy to use. I want to learn how to use it ~~",
        "date_posted": "January 5, 2026"        
    },
]


@app.get("/", include_in_schema=False, name="home")
@app.get("/posts", include_in_schema=False, name="posts")
def home(request: Request):
    return templates.TemplateResponse(request, "home.html", {"posts": posts, "title": "Home"})


@app.get("/api/posts")
def get_posts():
    return posts