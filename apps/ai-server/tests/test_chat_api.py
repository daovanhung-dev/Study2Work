import json
import unittest
from unittest.mock import patch

import httpx
from fastapi.testclient import TestClient

from app.main import app
from app.service.ai.ollama_service import ai_service


class ChatAPITests(unittest.TestCase):
    def setUp(self):
        self.requests = []
        self.clients = []
        self.limits = []
        self.reply = httpx.Response(200, json={"response": "ok"})
        original_client = httpx.AsyncClient

        def handler(request):
            self.requests.append(request)
            if isinstance(self.reply, Exception):
                raise self.reply
            return self.reply

        def factory(**kwargs):
            self.limits.append(kwargs["limits"])
            client = original_client(transport=httpx.MockTransport(handler), **kwargs)
            self.clients.append(client)
            return client

        self.patcher = patch("app.service.ai.ollama_service.httpx.AsyncClient", side_effect=factory)
        self.patcher.start()
        self.assertIsNone(ai_service._client)
        self.client = TestClient(app)
        self.client.__enter__()

    def tearDown(self):
        try:
            self.client.__exit__(None, None, None)
            self.assertTrue(all(client.is_closed for client in self.clients))
        finally:
            self.patcher.stop()

    def test_lifespan_and_success_contract(self):
        self.assertEqual(len(self.clients), 1)
        self.assertIs(ai_service._client, self.clients[0])
        self.assertEqual(self.limits[0].max_connections, 100)
        self.assertEqual(self.clients[0].timeout.pool, 5)
        self.assertEqual(self.client.get("/").status_code, 200)
        prompt = "  code\nprint(1)  "
        response = self.client.post("/api/v1/chat_log_ai", json={"prompt": prompt})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"response": "ok"})
        self.assertEqual(json.loads(self.requests[0].content), {
            "model": ai_service.model, "prompt": prompt, "stream": False
        })
        self.assertEqual(len(self.clients), 1)

    def test_prompt_validation_and_boundary(self):
        for body in [{}, {"prompt": 1}, {"prompt": ""}, {"prompt": "  \n\t"}, {"prompt": "x" * 8001}]:
            with self.subTest(body=str(body)[:30]):
                response = self.client.post("/api/v1/chat_log_ai", json=body)
                self.assertEqual(response.status_code, 422)
                self.assertIn("detail", response.json())
        self.assertEqual(self.requests, [])
        accepted = " " + "x" * 7998 + " "
        response = self.client.post("/api/v1/chat_log_ai", json={"prompt": accepted})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(self.requests[0].content)["prompt"], accepted)

    def test_upstream_error_contract(self):
        cases = [
            (httpx.PoolTimeout("SECRET_BODY"), 503, "AI_BUSY"),
            (httpx.ConnectError("SECRET_BODY"), 503, "OLLAMA_UNAVAILABLE"),
            (httpx.ConnectTimeout("SECRET_BODY"), 503, "OLLAMA_UNAVAILABLE"),
            (httpx.ReadTimeout("SECRET_BODY"), 504, "OLLAMA_TIMEOUT"),
            (httpx.Response(500, text="SECRET_BODY"), 502, "OLLAMA_BAD_RESPONSE"),
            (httpx.Response(200, text="bad json SECRET_BODY"), 502, "OLLAMA_BAD_RESPONSE"),
            (httpx.Response(200, json={"response": 5}), 502, "OLLAMA_BAD_RESPONSE"),
        ]
        for reply, expected_status, code in cases:
            with self.subTest(code=code, reply=type(reply).__name__):
                self.reply = reply
                response = self.client.post("/api/v1/chat_log_ai", json={"prompt": "SECRET_PROMPT"})
                self.assertEqual(response.status_code, expected_status)
                self.assertEqual(set(response.json()), {"error"})
                self.assertEqual(response.json()["error"]["code"], code)
                self.assertEqual(set(response.json()["error"]), {"code", "message"})
                self.assertNotIn("SECRET", response.text)
                self.assertNotIn("11434", response.text)


if __name__ == "__main__":
    unittest.main()
