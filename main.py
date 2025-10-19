import uvicorn
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

RAG_DATABASE = {
    "What does the author affectionately call the => syntax?": {
        "answer": "This is a popular syntax in other languages that the author affectionately calls the 'fat arrow'.",
        "sources": "TypeScript Book, Chapter: Functions"
    },
    "Which operator converts any value into an explicit boolean?": {
        "answer": "You can convert any value into an explicit boolean by using the '!!' operator (double negation).",
        "sources": "TypeScript Book, Chapter: Types"
    }
}

app = FastAPI(
    title="TechDocs RAG API",
    description="Searches TypeScript documentation."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/search")
async def search_rag(q: str = Query(..., description="The user's question")):
    
    result = RAG_DATABASE.get(q)
    
    if result:
        return result
    else:
        return JSONResponse(
            status_code=404,
            content={
                "answer": "Sorry, I don't have an answer for that specific question.",
                "sources": "N/A"
            }
        )
