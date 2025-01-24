from pathlib import Path
import pymupdf

from llama_parse import LlamaParse, ResultType


def pdf2md(pdf: Path, save_path: Path) -> str:
    """Convert a PDF to a markdown string."""  # TODO: use non-proprietary parser

    parser = LlamaParse(result_type=ResultType.MD)
    document = parser.load_data(str(pdf))

    md = "\n".join([doc.text for doc in document])
    with open(save_path, "w") as f:
        f.write(md)
    return md


def pdf2jpg(pdf_path: Path, save_path: Path) -> None:
    """Convert PDF into multiple JPG images."""

    save_path.mkdir(parents=True, exist_ok=True)
    with pymupdf.open(pdf_path) as pdf:
        for page in pdf:
            pix = page.get_pixmap()
            pix.save(save_path / f"{page.number}.jpg")
