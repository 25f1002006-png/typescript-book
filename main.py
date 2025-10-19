import uvicorn
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse, JSONResponse

# The database now stores only the raw answer strings
RAG_DATABASE = {
    "What syntax allows initializing class fields outside the constructor?": "The 'property initializer' syntax allows initializing class fields outside the constructor.",
    "What property name do discriminated unions use to narrow types?": "Discriminated unions commonly use the 'kind' property to narrow types.",
    "Which keyword pauses and resumes execution in generator functions?": "The 'yield' keyword is used to pause and resume execution in generator functions.",
    "What filename do you use to declare globals available across your entire TS project?": "You can use a 'global.d.ts' file to declare globals for your entire TS project.",
    "What TS helper wraps subclass constructors for ES5-style inheritance?": "The '__extends' helper function is used to wrap subclass constructors for ES5-style inheritance.",
    "What option in tsconfig.json turns on ES7 decorator support?": "To turn on ES7 decorator support, you set the 'experimentalDecorators' option in tsconfig.json.",
    "What directive in tsconfig.json preserves raw JSX output?": "The setting 'jsx: \"preserve\"' in tsconfig.json preserves the raw JSX output for another tool to process.",
    "In async/await, what wraps generator code to return a Promise?": "The '__awaiter' helper function wraps generator code to return a Promise for async/await.",
    "What npm package is recommended for structural deep-equality checks?": "For structural deep-equality checks, the 'deep-equal' npm package is often recommended."
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
        # Return the answer as raw plain text, not JSON
        return PlainTextResponse(content=result)
    else:
        # Return the error as JSON (as seen in the error log)
        return JSONResponse(
            status_code=404,
            content={
                "answer": "Sorry, I don't have an answer for that specific question.",
                "sources": "N/A"
            }
        )
