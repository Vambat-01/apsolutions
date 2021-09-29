from unittest import TestCase
import requests
from requests.models import Response


class SystemTest(TestCase):
    """
        Для запуска теста должны быть запущены web-приложение и Elastic.
    """
    def _get_documents(self, text: str) -> Response:
        response = requests.get(f"http://0.0.0.0:8000/documents?text={text}")
        self.assertEqual(response.status_code, 200)
        return response.json()

    def _delete_document(self, id: int) -> dict:
        response = requests.delete(f"http://0.0.0.0:8000/documents/{id}")
        self.assertEqual(response.status_code, 200)
        return response.json()

    def test_web_app(self):
        documents_1 = self._get_documents("по тебе")
        document = documents_1[0]
        self.assertTrue(document in documents_1)

        id = document["id"]
        self._delete_document(id)

        documents_2 = self._get_documents("по тебе")
        self.assertFalse(document in documents_2)
