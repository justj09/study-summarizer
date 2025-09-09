from typing import List
from langchain_openai import ChatOpenAI
from langchain_core.documents import Document
from pydantic import BaseModel, Field
from config import settings


class DocumentAnalysis(BaseModel):
    description: str = Field(
        description="Brief 2-3 sentence description of what this file is about"
    )
    summary: str = Field(
        description="Detailed 5-10 summary of the main content and key points"
    )


def analyze_documents(docs: List[Document]) -> DocumentAnalysis:
    """Analyze the list of documents using an OpenAI model for a description and summary."""

    combined_content = "\n\n".join([doc.page_content for doc in docs])
    try:
        llm = ChatOpenAI(model=settings.gpt_model, api_key=settings.openai_key)
        structured_llm = llm.with_structured_output(DocumentAnalysis, strict=True)
        prompt = f"Analyze this files contents and provide a structured response. Use plain text only, no markdown formatting.\n\nContent: {combined_content}"
        analysis = structured_llm.invoke(prompt)
        return analysis
    except Exception as e:
        raise e
