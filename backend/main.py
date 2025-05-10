from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse, JSONResponse
import os
from ast_parser import parse_code
from dot_render import generate_dot

PYTHON_EXAMPLES_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../python_examples'))

app = FastAPI()

# Allow CORS for local frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/list-python-files")
def list_python_files():
    files = [f for f in os.listdir(PYTHON_EXAMPLES_DIR) if f.endswith('.py')]
    return JSONResponse(files)

@app.get("/api/dot/{filename}")
def get_dot(filename: str):
    if not filename.endswith('.py'):
        raise HTTPException(status_code=400, detail="Invalid file type")
    file_path = os.path.join(PYTHON_EXAMPLES_DIR, filename)
    if not os.path.isfile(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    with open(file_path, 'r') as f:
        code = f.read()
    ast_dict = parse_code(code)
    dot = generate_dot(ast_dict)
    return PlainTextResponse(str(dot)) 