from recipes.server import create_app


async def test_hello(aiohttp_client):
    client = await aiohttp_client(create_app)

    resp = await client.get('/')
    assert resp.status == 200

    text = await resp.text()
    assert text.startswith('Hello,')
