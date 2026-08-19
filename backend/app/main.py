from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware

from app.api import all_routers


app = FastAPI(

    title="FatigueSense API",

    description=(
        "AI-based fatigue detection system "
        "using computer vision, RAG and LangChain"
    ),

    version="1.0.0"
)


app.add_middleware(

    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"]
)


for router in all_routers:

    app.include_router(router)


@app.get("/")
async def root():

    return {

        "message":
            "FatigueSense API is running",

        "docs":
            "/docs",

        "health":
            "/api/health"
    }