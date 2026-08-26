import io
import pymupdf


def extract_text_from_pdf(pdf_data: bytes) -> str:
    document = pymupdf.open(
        stream=io.BytesIO(pdf_data),
        filetype="pdf",
    )

    pages_text = []

    for page in document:
        pages_text.append(page.get_text())

    return "\n".join(pages_text).strip()