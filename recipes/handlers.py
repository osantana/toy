from uuid import uuid4

from staty import BadRequestException

from toy.handlers import Handler
from toy.http import JSONResponse

MAX_PAGE_SIZE = 50


class Recipes(Handler):
    def get(self, request):
        try:
            offset = int(request.query_string.get('offset', [0])[-1])
            limit = int(request.query_string.get('limit', [MAX_PAGE_SIZE])[-1])
            limit = min(MAX_PAGE_SIZE, limit)
        except ValueError:
            raise BadRequestException('Invalid limit/offset value.')

        result = {
            'total': 1,
            'count': limit,
            'offset': offset,
            'results': [
                {
                    'id': str(uuid4()),
                    'name': 'Salad',
                    'prep_time_in_minutes': 5,
                    'difficulty': 1,
                    'vegetarian': True,
                }
            ],
        }

        return JSONResponse(result)


class Recipe(Handler):
    pass
