from routers.order_router import router


def test_order_router_exists():
    assert router is not None
    assert any(route.path == "/orders/" for route in router.routes)
