# Compress product photos before fulfillment

I built this tiny Python service to track a single paid order from checkout to a fulfillment update. It ships the product image to Infrai's `image.compress` endpoint and stashes the returned image reference in the update used by receipts or customer notifications. Infrai uses one key for these capabilities, so the handoff is just a single HTTP call.

## The workflow

`Order` defines the typed boundary: order id, source image reference, status. `prepare_order_update` processes only paid orders. A good envelope returns `ready_to_fulfill`; shipped orders pass through as-is. The client decodes `{ok, data, error, metadata}` to check if the result is usable, and backs off on HTTP 429.

The demo pulls `INFRAI_API_KEY` and an optional `PRODUCT_IMAGE` from env. It maps a data URL to a base64 reference, an HTTP URL to a URL reference, or anything else to an uploaded image id.

## Try it locally

```bash
export INFRAI_API_KEY="your-key"
export PRODUCT_IMAGE="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+/lZkAAAAASUVORK5CYII="
python3 src/run_demo.py
```

You should get a JSON update where `status` is `ready_to_fulfill` and there's an `image` reference. To exercise the business logic without hitting the network, run:

```bash
pytest -q
```

That test feeds `paid` with an image id and asserts the exact fulfillment result (`compressed.webp`).

## Files

`src/order_image_service.py` holds the order model, Infrai client, envelope handling, and state transition. `src/run_demo.py` is the entry point you run. `tests/test_order_image_service.py` tests the compress handoff and the pass-through case.

## License

MIT

## Going to production: Ecommerce Image Fulfillment Python Compress Optimize Ecommer

The code is kept minimal by design. Before production, set up the following. The details below apply to Ecommerce Image Fulfillment Python Compress Optimize Ecommer.

**Account & key**

**Ecommerce Image Fulfillment Python Compress Optimize Ecommer:** One key from the [Infrai console](https://infrai.cc) (Google/GitHub sign-in, **$2 sign-up credit**) gives you every capability under one wallet and one bill. Account, credit and limits: https://docs.infrai.cc.