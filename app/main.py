from pathlib import Path
from fastapi import Depends, FastAPI, File, Form, HTTPException, UploadFile
from pydantic import BaseModel
from .dependencies import get_api_key
from .utils import analyze_content, load_pdf_content
from config import settings


class PagedModel(BaseModel):
    start_page: int
    end_page: int


app = FastAPI(
    title="Study Summarizer",
    dependencies=[Depends(get_api_key)]
)


@app.post("/analyze/", summary="Generate a summary and description for a PDF file within a page range.", tags=["PDF Analysis"])
async def analyze(
    file: UploadFile = File(..., description="PDF file to analyze"),
    start_page: int = Form(..., description="First page of range"),
    end_page: int = Form(..., description="Last page of range")
):
    if file.size > settings.max_file_size_mb * 1024 * 1024:
        raise HTTPException(status_code=413, detail=f"File too large (max {settings.max_file_size_mb} MB)")
    
    if min(start_page, end_page) <= 0:
        raise HTTPException(status_code=400, detail=f"Page number must be postive")
    
    if end_page - start_page > settings.max_page_count:
        raise HTTPException(status_code=400, detail=f"Page count too large (max {settings.max_page_count} pages)")
    
    temp_file = Path(settings.temp_folder, file.filename)
    temp_file.parent.mkdir(exist_ok=True)
    
    try:
        with open(temp_file, "wb") as f:
            file_bytes = await file.read() 
            f.write(file_bytes)
        
        content = load_pdf_content(temp_file, start_page, end_page)
        analysis = analyze_content(content)
        temp_file.unlink(missing_ok=True)

        return {"summary": analysis.summary, "description": analysis.description}

    except Exception as e:
        temp_file.unlink(missing_ok=True)
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
