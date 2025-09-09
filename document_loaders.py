from io import BytesIO
from google.cloud import vision
from google.oauth2 import service_account
from PIL.Image import Image
from langchain_community.document_loaders.parsers.pdf import PyMuPDFParser
from langchain_community.document_loaders.parsers.images import BaseImageBlobParser
from langchain_community.document_loaders.pdf import PyMuPDFLoader
from config import settings


class GoogleOCRImageBlobParser(BaseImageBlobParser):
    """Parser for extracting text from images using Google Vision OCR."""

    def __init__(self):
        super().__init__()
        credentials = service_account.Credentials.from_service_account_info(
            settings.google_credentials
        )
        self.client = vision.ImageAnnotatorClient(credentials=credentials)

    def _analyze_image(self, img: Image) -> str:
        image_bytes = BytesIO()
        img.save(image_bytes, format="PNG")
        image_bytes = image_bytes.getvalue()

        image = vision.Image(content=image_bytes)
        features = [vision.Feature(type=vision.Feature.Type.DOCUMENT_TEXT_DETECTION)]
        request = vision.AnnotateImageRequest(image=image, features=features)
        response = self.client.annotate_image(request)

        if response.error.message:
            raise Exception(f"Google Vision API error: {response.error.message}")

        text = response.full_text_annotation.text
        return text.strip() if text else ""


class CustomPDFLoader(PyMuPDFLoader):
    """Load and parse a PDF file comprehensively."""

    def __init__(self, file_path, **kwargs):
        kwargs.setdefault("extract_images", True)
        kwargs.setdefault("images_parser", GoogleOCRImageBlobParser())
        kwargs.setdefault("extract_tables", "csv")
        super().__init__(file_path, **kwargs)
