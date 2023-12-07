from pydantic import BaseModel, Field, validator
from typing import List, Dict
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter


# 继承Pydantic BaseModel
class Date(BaseModel):
    year: int = Field(description="Year")
    month: int = Field(description="Month")
    day: int = Field(description="day")
    era: str = Field(description="BC or AD")

    # 可选的添加校验机制
    @validator("month")
    def valid_month(cls, field):
        if field <= 0 or field > 12:
            raise ValueError("月份必须在1-12之间")
        return field

    @validator("day")
    def valid_day(cls, field):
        if field <= 0 or field > 31:
            raise ValueError("日期必须在1-31之间")
        return field

    @validator("day", pre=True, always=True)
    def valid_date(cls, day, values):
        year = values.get("year")
        month = values.get("month")
        if year is None or month is None:
            return day  # 无法验证日期

        if month == 2:
            if cls.is_leap_year(year) and day > 29:
                raise ValueError("闰年2月份最多29天")
            elif not cls.is_leap_year(year) and day > 28:
                raise ValueError("平年2月份最多28天")
        elif month in [4, 6, 9, 11] and day > 30:
            raise ValueError("{month}月份最多30天")

        return day

    @staticmethod
    def is_leap_year(year):
        if year % 4 == 0 or (year % 4 == 0 and year % 100 != 0):
            return True
        return False


def extract_text_by_page(filename):
    pdfloader = PyPDFLoader(filename)
    pages = pdfloader.load_and_split()
    return [page.page_content for page in pages]


def get_lines_from_pages(pages):
    return [line for page in pages for line in page.split("\n")]


def get_paragraph(lines, min_line_length=10):
    paragraphs = []
    buffer = ""
    for line in lines:
        if len(line) >= min_line_length:  # 这是在一段的内容之中
            buffer += (" " + line) if not line.endswith("-") else line.strip("-")
        elif buffer:  # 这是一段结束
            buffer += " " + line
            paragraphs.append(buffer)
            buffer = ""
        else:  # 这是当一段开始，字数即小于min_line_length的情况
            paragraphs.append(line)
    if buffer:
        paragraphs.append(buffer)
    return paragraphs


# pages = extract_text_by_page("zhihu_ai_homework/RAG/llama2-test-1-4.pdf")
# para = get_paragraph(get_lines_from_pages(pages), min_line_length=15)

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=200, chunk_overlap=50, length_function=len, add_start_index=True
)


def get_paragraphs_bylangchain(pageList):
    return text_splitter.create_documents(pageList)
