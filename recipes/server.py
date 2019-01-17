import asyncio

from aiohttp import web
from prettyconf import config


async def handle(request):
    dburl = config('DATABASE_URL')
    name = request.match_info.get('name', 'Anonymous')
    text = 'Hello, ' + name + 'you are opening database at ' + dburl

    return web.Response(text=text)


# noinspection PyShadowingNames
def create_app(loop):
    app = web.Application(loop=loop)
    app.add_routes([
        web.get('/', handle),
        web.get('/{name}', handle),
    ])
    return app


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    app = create_app(loop=loop)
    web.run_app(app)
