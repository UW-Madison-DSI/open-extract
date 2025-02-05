from pathlib import Path
import pymupdf
import openparse
import pymupdf4llm
from llama_parse import LlamaParse, ResultType
from markitdown import MarkItDown


def pdf2md_llamaparse(pdf: Path, save_path: Path) -> str:
    """Convert a PDF to a markdown string. (External API, not recommended)"""

    parser = LlamaParse(result_type=ResultType.MD)
    document = parser.load_data(str(pdf))

    md = "\n".join([doc.text for doc in document])
    save_path.write_text(md)
    return md


def pdf2md_markitdown(pdf: Path, save_path: Path) -> str:
    """Use Markitdown to convert a PDF to a markdown string. (Poor quality, not recommended)"""

    result = MarkItDown().convert(str(pdf))
    md = result.text_content
    save_path.write_text(md)
    return md


def pdf2txt(pdf_path: Path, save_path: Path) -> str:
    """Convert a PDF to a text string. (Interesting nodes output, explore later.)"""

    parsed_doc = openparse.DocumentParser().parse(pdf_path)
    text = "\n\n".join([node.text for node in parsed_doc.nodes])
    save_path.write_text(text)
    return text


def pdf2md(pdf: Path, save_path: Path) -> str:
    """Convert a PDF to a markdown string with pymupdf."""

    md = pymupdf4llm.to_markdown(pdf)
    save_path.write_text(md)
    return md


def pdf2jpg(pdf_path: Path, save_path: Path) -> None:
    """Convert PDF into multiple JPG images."""

    save_path.mkdir(parents=True, exist_ok=True)
    with pymupdf.open(pdf_path) as pdf:
        for page in pdf:
            pix = page.get_pixmap()
            pix.save(save_path / f"{page.number}.jpg")
