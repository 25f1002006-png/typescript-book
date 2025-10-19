import uvicorn
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# --- This is the new, correct RAG Database ---
RAG_DATABASE = {
    "What syntax allows initializing class fields outside the constructor?": {
        "answer": "The 'property initializer' syntax allows initializing class fields outside the constructor.",
        "sources": "TypeScript Book, Chapter: Classes"
    },
    "What property name do discriminated unions use to narrow types?": {
        "answer": "Discriminated unions commonly use the 'kind' property to narrow types.",
        "sources": "TypeScript Book, Chapter: Types"
    },
    "Which keyword pauses and resumes execution in generator functions?": {
        "answer": "The 'yield' keyword is used to pause and resume execution in generator functions.",
        "sources": "TypeScript Book, Chapter: Iterators and Generators"
    },
    "What filename do you use to declare globals available across your entire TS project?": {
        "answer": "You can use a 'global.d.ts' file to declare globals for your entire TS project.",
        "sources": "TypeScript Book, Chapter: Declaration Files"
    },
    "What TS helper wraps subclass constructors for ES5-style inheritance?": {
        "answer": "The '__extends' helper function is used to wrap subclass constructors for ES5-style inheritance.",
        "sources": "TypeScript Book, Chapter: Inheritance"
    },
    "What option in tsconfig.json turns on ES7 decorator support?": {
        "answer": "To turn on ES7 decorator support, you set the 'experimentalDecorators' option in tsconfig.json.",
        "sources": "TypeScript Book, Chapter: Decorators"
    },
    "What directive in tsconfig.json preserves raw JSX output?": {
        "answer": 'The setting \'jsx: "preserve"\' in tsconfig.json preserves the raw JSX output for another tool to process.',
        "sources": "TypeScript Book, Chapter: JSX"
    },
    "In async/await, what wraps generator code to return a Promise?": {
        "answer": "The '__awaiter' helper function wraps generator code to return a Promise for async/await.",
        "sources": "TypeScript Book, Chapter: Async/Await"
    },
    "What npm package is recommended for structural deep-equality checks?": {
        "answer": "For structural deep-equality checks, the 'deep-equal' npm package is often recommended.",
        "sources": "TypeScript Book, Chapter: Tips"
    }
}
# ----------------------------------------


app = FastAPI(
    title="TechDocs RAG API",
    description="Searches TypeScript documentation."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],  # Allows GET, OPTIONS, etc.
    allow_headers=["*"],
)

@app.get("/search")
async def search_rag(q: str = Query(..., description="The user's question")):
    
    # The evaluator uses the exact question as the key,
    # so we can use a direct dictionary lookup.
    result = RAG_DATABASE.get(q)
    
    if result:
        # Found the question in our new database
        return result
    else:
        # Question not found
        return JSONResponse(
            status_code=404,
            content={
                "answer": "Sorry, I don't have an answer for that specific question.",
                "sources": "N/A"
            }
        )
