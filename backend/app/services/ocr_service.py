import io
from typing import Dict, Any, List, Tuple
from app.core.config import settings
from app.core.logging import logger

# Conditional imports
try:
    import fitz  # PyMuPDF
    PYMUPDF_AVAILABLE = True
except ImportError:
    PYMUPDF_AVAILABLE = False

try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

try:
    import pytesseract
    PYTESSERACT_AVAILABLE = True
except ImportError:
    PYTESSERACT_AVAILABLE = False


class OCRService:
    """
    Extracts text from PDF documents and images using PyMuPDF and Tesseract OCR.
    Never fabricates OCR text.
    """

    def is_ocr_installed(self) -> bool:
        if not (PIL_AVAILABLE and PYTESSERACT_AVAILABLE):
            return False
        try:
            # Quick check if tesseract binary responds
            pytesseract.get_tesseract_version()
            return True
        except Exception:
            return False

    def extract_text_from_document(
        self,
        file_bytes: bytes,
        file_type: str
    ) -> Tuple[str, List[Dict[str, Any]], Dict[str, Any]]:
        """
        Extracts embedded or OCR text page by page.
        Returns:
            full_text (str)
            pages_data (list of dicts with page_number, text, extraction_method)
            metadata (dict of processing details)
        """
        pages_data = []
        full_text_parts = []
        ocr_engine_used = "none"

        normalized_type = file_type.lower().replace(".", "")

        if normalized_type == "pdf":
            if not PYMUPDF_AVAILABLE:
                logger.error("PyMuPDF (fitz) is not installed.")
                return "", [], {"status": "failed", "error": "PyMuPDF library is not available."}

            try:
                doc = fitz.open(stream=file_bytes, filetype="pdf")
                tesseract_ready = self.is_ocr_installed()

                for page_idx in range(len(doc)):
                    page = doc[page_idx]
                    page_num = page_idx + 1
                    page_text = page.get_text() or ""

                    method = "pdf_embedded_text"

                    # If page has minimal text and OCR is available, attempt OCR on page render
                    if len(page_text.strip()) < 40 and tesseract_ready and PIL_AVAILABLE:
                        try:
                            pix = page.get_pixmap(dpi=200)
                            img = Image.open(io.BytesIO(pix.tobytes("png")))
                            ocr_text = pytesseract.image_to_string(img)
                            if len(ocr_text.strip()) > len(page_text.strip()):
                                page_text = ocr_text
                                method = "tesseract_ocr_rendered_page"
                                ocr_engine_used = "tesseract"
                        except Exception as e:
                            logger.warning(f"OCR page render failed for page {page_num}: {e}")

                    full_text_parts.append(page_text)
                    pages_data.append({
                        "page_number": page_num,
                        "text": page_text,
                        "method": method
                    })
                doc.close()

            except Exception as e:
                logger.error(f"Failed to parse PDF document: {str(e)}")
                return "", [], {"status": "failed", "error": f"PDF parse error: {str(e)}"}

        elif normalized_type in ["png", "jpg", "jpeg"]:
            if not PIL_AVAILABLE:
                return "", [], {"status": "failed", "error": "Pillow image library is not available."}

            try:
                image = Image.open(io.BytesIO(file_bytes))
                tesseract_ready = self.is_ocr_installed()

                if tesseract_ready:
                    extracted_text = pytesseract.image_to_string(image)
                    ocr_engine_used = "tesseract"
                    method = "tesseract_ocr_image"
                else:
                    extracted_text = ""
                    method = "ocr_executable_not_found"
                    logger.warning("Tesseract OCR is not installed or configured on the system.")

                full_text_parts.append(extracted_text)
                pages_data.append({
                    "page_number": 1,
                    "text": extracted_text,
                    "method": method
                })

            except Exception as e:
                logger.error(f"Failed to process image file: {str(e)}")
                return "", [], {"status": "failed", "error": f"Image processing error: {str(e)}"}

        combined_text = "\n\n".join(full_text_parts).strip()
        metadata = {
            "status": "completed" if combined_text else "needs_review",
            "ocr_engine": ocr_engine_used,
            "total_pages": len(pages_data),
            "character_count": len(combined_text)
        }

        return combined_text, pages_data, metadata


ocr_service = OCRService()
