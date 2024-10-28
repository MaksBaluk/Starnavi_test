import os

from google.api_core.exceptions import GoogleAPICallError
from google.cloud import language_v1
from google.oauth2 import service_account
from src.core.config import settings


def initialize_client() -> language_v1.LanguageServiceClient:
    credentials = service_account.Credentials.from_service_account_file(
        settings.GOOGLE_API_KEY
    )
    return language_v1.LanguageServiceClient(credentials=credentials)


def is_toxic_content(text: str) -> bool:
    client = initialize_client()

    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)

    try:
        response = client.analyze_sentiment(request={'document': document})

        if response.document_sentiment.score < 0:
            return True
        return False

    except GoogleAPICallError as e:
        print(f"Error calling Google Cloud Natural Language API: {e}")
        return False
