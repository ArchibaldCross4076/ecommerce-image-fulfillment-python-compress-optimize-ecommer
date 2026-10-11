from order_image_service import InfraiClient, Order, prepare_order_update


class StubClient(InfraiClient):
    def __init__(self):
        pass

    def compress(self, image):
        assert image == {"image_id": "original.jpg"}
        return {"ok": True, "data": {"image": "compressed.webp"}, "error": None, "metadata": {}}


def test_paid_order_moves_to_fulfillment_with_compressed_image():
    update = prepare_order_update(Order("ord-7", {"image_id": "original.jpg"}), StubClient())
    assert update == {"order_id": "ord-7", "status": "ready_to_fulfill", "image": "compressed.webp"}


def test_shipped_order_is_left_untouched():
    update = prepare_order_update(Order("ord-8", {"image_id": "original.jpg"}, "shipped"), StubClient())
    assert update == {"order_id": "ord-8", "status": "shipped"}
