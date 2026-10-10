import os
from typing import List, Optional
from pydantic import BaseModel, Field
from langchain_google_genai import ChatGoogleGenerativeAI
from pypdf import PdfReader


class Experience(BaseModel):
    title: str = Field(description="Job title")
    company: Optional[str] = Field(default=None)
    duration: Optional[str] = Field(default=None, description="e.g. '2022-2024'")


class Education(BaseModel):
    degree: str = Field(description="Degree name")
    institution: Optional[str] = Field(default=None)
    year: Optional[str] = Field(default=None)


class CVData(BaseModel):
    name: Optional[str] = Field(default=None)
    email: Optional[str] = Field(default=None)
    skills: List[str] = Field(default_factory=list)
    experience: List[Experience] = Field(default_factory=list)
    education: List[Education] = Field(default_factory=list)
    languages: List[str] = Field(default_factory=list)


def extract_text_from_pdf(file_field) -> str:
    file_field.open("rb")
    try:
        reader = PdfReader(file_field)
        text = "\n".join(page.extract_text() or "" for page in reader.pages)
    finally:
        file_field.close()
    return text.strip()


def parse_cv_text(text: str) -> CVData:
    llm = ChatGoogleGenerativeAI(
        model="gemini-3.8-flash",
        google_api_key=os.getenv("GEMINI_API_KEY"),
        temperature=0,
    )
    structured_llm = llm.with_structured_output(CVData)

    prompt = (
        "Extract structured information from the following resume text. "
        "Only use information explicitly present in the text — never invent data. "
        "If a field is not mentioned, leave it empty.\n\n"
        f"Resume text:\n{text}"
    )

    return structured_llm.invoke(prompt)