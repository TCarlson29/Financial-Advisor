from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow your React dev server to talk to this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/items")
async def get_items():
    return [{"id": 1, "name": "Foo"}, {"id": 2, "name": "Bar"}]