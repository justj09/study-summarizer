from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
from config import settings


class DocumentAnalysis(BaseModel):
    description: str = Field(
        description="Brief 2-3 sentence description of what the content is about"
    )
    summary: str = Field(
        description="Detailed 5-10 summary of the main content and key points"
    )


def analyze_content(content: str) -> DocumentAnalysis:
    """Analyze the content using an OpenAI model for an overall description and summary."""

    try:
        llm = ChatOpenAI(model=settings.gpt_model, api_key=settings.openai_key)
        structured_llm = llm.with_structured_output(DocumentAnalysis, strict=True)
        prompt = f"Analyze the content and provide a structured response. Use plain text only, no markdown formatting.\n\nContent: {content}"
        analysis = structured_llm.invoke(prompt)
        return analysis
    except Exception as e:
        raise e
