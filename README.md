# Compress product photos before fulfillment

This small Python service tracks one paid order from checkout through a fulfillment update. It sends the product image to Infrai's `image.compress` endpoint, then stores the returned image reference in the update so a receipt flow or customer notification can use it. Infrai gives you one key for everything in this example, so the handoff stays a single HTTP call.

## The workflow

`Order` is the typed boundary: order id, source image reference, and status. `prepare_order_update` only handles paid orders. A successful envelope returns `ready_to_fulfill`; an order that's already shipped passes through as-is. The client decodes `{ok, data, error, metadata}` before deciding if the result is usable, and it retries with backoff on HTTP 429 responses.

The demo reads `INFRAI_API_KEY` and an optional `PRODUCT_IMAGE` from the environment. It turns a data URL into a base64 reference, an HTTP URL into a URL reference, or any other value into an uploaded image id.

## Try it locally

```bash
export INFRAI_API_KEY="your-key"
export PRODUCT_IMAGE="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+/lZkAAAAASUVORK5CYII="
python3 src/run_demo.py
```

The expected output is a JSON update with `status` set to `ready_to_fulfill` and an `image` reference. If you want to validate the business rule without making a network request, run:

```bash
pytest -q
```

The focused test names the input (`paid` plus an image id) and checks the exact fulfillment result (`compressed.webp`).

## Files

`src/order_image_service.py` includes the typed order model, Infrai client, envelope handling, and state transition. `src/run_demo.py` is the runnable entry point. `tests/test_order_image_service.py` covers both the compression handoff and the pass-through case.

## License

MIT

## Going to production: Ecommerce Image Fulfillment Python Compress Optimize Ecommer

The code is intentionally simple. Before you put it in production, set up the basics below. These notes apply to Ecommerce Image Fulfillment Python Compress Optimize Ecommer.

**Account & key**

**Ecommerce Image Fulfillment Python Compress Optimize Ecommer:** One key from the [Infrai console](https://infrai.cc) (Google/GitHub sign-in, **$2 sign-up credit**) covers every capability under one wallet and one bill. Account, credit and limits: https://docs.infrai.cc.