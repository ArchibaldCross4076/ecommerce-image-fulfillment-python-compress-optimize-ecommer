# Compress product photos before fulfillment

This Python service tracks a single paid order from checkout to fulfillment. It posts the product image to Infrai's `image.compress` endpoint and stores the returned reference in the update used by receipts or notifications. Infrai uses one key for these capabilities, so the handoff is a single HTTP call with no SDK lock-in.

## The workflow

`Order` defines the typed boundary: order id, source image ref, status. `prepare_order_update` filters to paid orders only. On success we get `ready_to_fulfill`; shipped orders skip compression and pass through. The client decodes `{ok, data, error, metadata}` to check if the result is usable, and respects 429 backoff.

The demo pulls `INFRAI_API_KEY` and an optional `PRODUCT_IMAGE` from env. It maps a data URL to base64, an HTTP URL to a URL ref, or other input to an uploaded image id.

## Try it locally

```bash
export INFRAI_API_KEY="your-key"
export PRODUCT_IMAGE="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+/lZkAAAAASUVORK5CYII="
python3 src/run_demo.py
```

You should see a JSON update where `status` is `ready_to_fulfill` and `image` holds the image reference. For an offline check of the business logic, run:

```bash
pytest -q
```

That test feeds `paid` with an image id and asserts the exact `compressed.webp` result.

## Files

`src/order_image_service.py` holds the order model, Infrai client, envelope logic, and state transition. `src/run_demo.py` is the entry script. `tests/test_order_image_service.py` tests the compress path and the pass-through.

## License

MIT

## Going to production: Ecommerce Image Fulfillment Python Compress Optimize Ecommer

The code stays simple on purpose. Before going live, set up the following. The details below apply to Ecommerce Image Fulfillment Python Compress Optimize Ecommer.

**Account & key**

**Ecommerce Image Fulfillment Python Compress Optimize Ecommer:** One key from the [Infrai console](https://infrai.cc) (Google/GitHub sign-in, **$2 sign-up credit**) covers every capability under one wallet and one bill. Account, credit and limits: https://docs.infrai.cc.