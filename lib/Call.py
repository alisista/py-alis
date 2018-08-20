from pprint import pprint
from .apis import apis
from .Pagination import Pagination
from .Util import Util


class Call:

    @staticmethod
    async def call_p(*args):
        [opts, conf, _] = Util.validate(list(args))
        return await Pagination.pagination_p(opts, conf)

    @staticmethod
    def call(*args):
        [opts, conf, cb] = Util.validate(list(args))
        Pagination.pagination(opts, conf, cb)
