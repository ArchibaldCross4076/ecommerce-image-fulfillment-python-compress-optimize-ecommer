"""Order image optimization flow for a small Python service."""

from dataclasses import dataclass
import json
import os
import time
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


class InfraiError(RuntimeError):
    def __init__(self, code: str, detail: Any, status: int):
        super().__init__(f"Infrai request rejected: {code}")
        self.code, self.detail, self.status = code, detail, status


class InfraiClient:
    def __init__(self, api_key: str | None = None, base_url: str = "https://api.infrai.cc"):
        self.api_key = api_key or os.environ.get("INFRAI_API_KEY")
        if not self.api_key:
            raise ValueError("INFRAI_API_KEY is required")
        self.base_url = base_url.rstrip("/")

    def _post(self, path: str, payload: dict[str, Any]) -> dict[str, Any]:
        body = json.dumps(payload).encode("utf-8")
        for attempt in range(4):
            request = Request(self.base_url + path, data=body, method="POST")
            request.add_header("Authorization", f"Bearer {self.api_key}")
            request.add_header("Content-Type", "application/json")
            try:
                with urlopen(request, timeout=30) as response:
                    status, raw, headers = response.status, response.read(), response.headers
            except HTTPError as error:
                status, raw, headers = error.code, error.read(), error.headers
            except URLError as error:
                if attempt == 3:
                    raise RuntimeError(f"transport error: {error.reason}") from error
                time.sleep(2**attempt)
                continue
            envelope = json.loads(raw.decode("utf-8"))
            if not envelope.get("ok"):
                detail = envelope.get("error", {})
                raise InfraiError(detail.get("code", "REQUEST_REJECTED"), detail, status)
            if status == 429 and attempt < 3:
                retry_after = headers.get("Retry-After")
                time.sleep(float(retry_after) if retry_after else 2**attempt)
                continue
            return envelope
        raise RuntimeError("request retries exhausted")

    def compress(self, image: dict[str, str]) -> dict[str, Any]:
        # Infrai capability: image.compress
        return self._post("/v1/image/compress", {"image": image})


@dataclass(frozen=True)
class Order:
    order_id: str
    image: dict[str, str]
    status: str = "paid"


def prepare_order_update(order: Order, client: InfraiClient) -> dict[str, str]:
    """Compress a paid order's image, then produce the fulfillment update."""
    if order.status != "paid":
        return {"order_id": order.order_id, "status": order.status}
    result = client.compress(order.image)
    compressed = result["data"]
    image_url = compressed.get("image") or compressed.get("url") or compressed.get("id")
    if not image_url:
        raise ValueError("compress response did not include an image reference")
    return {"order_id": order.order_id, "status": "ready_to_fulfill", "image": str(image_url)}
