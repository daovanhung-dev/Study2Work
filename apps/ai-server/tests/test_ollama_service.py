import asyncio
import json
import os
import unittest
from unittest.mock import patch

import httpx

from app.service.ai.ollama_service import (
    AIBusyError,
    AIConnectionError,
    AIResponseError,
    AITimeoutError,
    OllamaService,
)


class OllamaServiceTests(unittest.IsolatedAsyncioTestCase):
    async def test_explicit_lifecycle_reuses_one_client_for_concurrent_calls(self):
        clients = []
        limits = []
        requests = []
        original_client = httpx.AsyncClient

        async def handler(request):
            requests.append(request)
            await asyncio.sleep(0)
            if request.url.path == "/api/tags":
                return httpx.Response(200, json={"models": [{"name": "demo"}]})
            if request.url.path == "/api/chat":
                return httpx.Response(200, json={"message": {"content": "chat"}})
            prompt = json.loads(request.content)["prompt"]
            return httpx.Response(200, json={"response": prompt})

        def factory(**kwargs):
            limits.append(kwargs["limits"])
            client = original_client(transport=httpx.MockTransport(handler), **kwargs)
            clients.append(client)
            return client

        service = OllamaService(base_url="http://ollama.test")
        with patch("app.service.ai.ollama_service.httpx.AsyncClient", side_effect=factory):
            with self.assertRaisesRegex(RuntimeError, "start"):
                await service.generate("before start")
            await service.start()
            await service.start()
            try:
                first, second = await asyncio.gather(
                    service.generate("first"), service.generate("second")
                )
                self.assertEqual((first["answer"], second["answer"]), ("first", "second"))
                self.assertEqual((await service.chat([{"role": "user", "content": "hi"}]))["answer"], "chat")
                self.assertEqual(await service.list_models(), ["demo"])
                self.assertTrue((await service.health_check())["available"])
                self.assertEqual(len(clients), 1)
                self.assertEqual(len(requests), 5)
                self.assertEqual(clients[0]._transport.__class__, httpx.MockTransport)
                self.assertEqual(limits[0].max_connections, 100)
                self.assertEqual(clients[0].timeout.pool, 5.0)
            finally:
                await service.close()
            self.assertTrue(clients[0].is_closed)
            with self.assertRaisesRegex(RuntimeError, "start"):
                await service.generate("after close")

    async def test_configured_timeout_keeps_separate_pool_wait(self):
        with patch.dict(os.environ, {"OLLAMA_TIMEOUT": "12"}):
            service = OllamaService()
        await service.start()
        try:
            self.assertEqual(service._client.timeout.connect, 12)
            self.assertEqual(service._client.timeout.read, 12)
            self.assertEqual(service._client.timeout.write, 12)
            self.assertEqual(service._client.timeout.pool, 5)
        finally:
            await service.close()

    async def test_transport_errors_are_classified_without_raw_details(self):
        cases = [
            (httpx.PoolTimeout, AIBusyError),
            (httpx.ConnectError, AIConnectionError),
            (httpx.ConnectTimeout, AIConnectionError),
            (httpx.ReadError, AIConnectionError),
            (httpx.ReadTimeout, AITimeoutError),
            (httpx.WriteTimeout, AITimeoutError),
            (httpx.RemoteProtocolError, AIResponseError),
        ]
        original_client = httpx.AsyncClient
        for upstream_error, mapped_error in cases:
            with self.subTest(upstream_error=upstream_error.__name__):
                def handler(request):
                    raise upstream_error("SECRET_UPSTREAM_BODY")

                with patch("app.service.ai.ollama_service.httpx.AsyncClient", side_effect=lambda **kwargs: original_client(transport=httpx.MockTransport(handler), **kwargs)):
                    service = OllamaService()
                    await service.start()
                    try:
                        with self.assertLogs("app.service.ai.ollama_service", level="WARNING") as logs:
                            with self.assertRaises(mapped_error) as caught:
                                await service.generate("SECRET_PROMPT")
                        self.assertNotIn("SECRET", str(caught.exception))
                        self.assertNotIn("SECRET", " ".join(logs.output))
                    finally:
                        await service.close()

    async def test_invalid_upstream_payload_is_bad_response(self):
        responses = [
            httpx.Response(500, text="SECRET_UPSTREAM_BODY"),
            httpx.Response(200, text="broken json"),
            httpx.Response(200, json=[]),
            httpx.Response(200, json={"done": True}),
            httpx.Response(200, json={"response": 123}),
        ]
        original_client = httpx.AsyncClient
        for upstream_response in responses:
            with self.subTest(response=upstream_response.status_code, body=upstream_response.content):
                with patch("app.service.ai.ollama_service.httpx.AsyncClient", side_effect=lambda **kwargs: original_client(transport=httpx.MockTransport(lambda request: upstream_response), **kwargs)):
                    service = OllamaService()
                    await service.start()
                    try:
                        with self.assertRaises(AIResponseError) as caught:
                            await service.generate("SECRET_PROMPT")
                        self.assertNotIn("SECRET", str(caught.exception))
                    finally:
                        await service.close()

    async def test_direct_caller_closes_client_even_if_request_fails(self):
        original_client = httpx.AsyncClient
        service = OllamaService()
        with patch("app.service.ai.ollama_service.httpx.AsyncClient", side_effect=lambda **kwargs: original_client(transport=httpx.MockTransport(lambda request: httpx.Response(502)), **kwargs)):
            await service.start()
            client = service._client
            try:
                with self.assertRaises(AIResponseError):
                    await service.generate("x")
            finally:
                await service.close()
            self.assertTrue(client.is_closed)
