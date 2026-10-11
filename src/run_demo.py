import json
import os

from order_image_service import InfraiClient, Order, prepare_order_update


def main() -> None:
    client = InfraiClient()
    source = os.environ.get("PRODUCT_IMAGE", "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+/lZkAAAAASUVORK5CYII=")
    if source.startswith("data:"):
        image = {"base64": source.split(",", 1)[1]}
    elif source.startswith(("https://", "http://")):
        image = {"url": source}
    else:
        image = {"image_id": source}
    order = Order(order_id="demo-1001", image=image)
    print(json.dumps(prepare_order_update(order, client), indent=2))


if __name__ == "__main__":
    main()
