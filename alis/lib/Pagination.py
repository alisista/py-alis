from .apis import apis
from .Request import Request
from .Util import Util


class Response:
    def __init__(self, opts, conf, json, url, cb):
        self.opts = opts
        self.conf = conf
        self.json = json
        self.url = url
        self.cb = cb
        self.LEK = self.json.get("LastEvaluatedKey") or {}
        self.itemCount = len(self.json.get("Items") or [])
        if apis[conf["path_name"]][conf.get("method") or "get"].get("by_page"):
            self.isNext = self.itemCount >= (self.opts.get("limit") or 20)
        else:
            self.isNext = False if not self.LEK else True
        self.itemCount = len(self.json.get("Items") or [])
        if self.itemCount == 0:
            self.startNth = 0
            self.endNth = 0
        else:
            self.startNth = 1 if not self.conf.get("endNth") else self.conf.get("endNth") + 1
            self.endNth = self.startNth + self.itemCount - 1

    def cp_params(self, opts, opts2):

        for k in opts2:
            opts[k] = opts2[k]
        if apis[self.conf["path_name"]][self.conf.get("method") or "get"].get("by_page"):
            opts["page"] = (self.opts.get("page") or 1) + 1
        else:
            opts["sort_key"] = self.LEK.get("sort_key")
            opts["article_id"] = self.LEK.get("article_id")
            opts["comment_id"] = self.LEK.get("comment_id")
            opts["notification_id"] = self.LEK.get("notification_id")
            opts["score"] = self.LEK.get("score")
            opts["evaluated_at"] = self.LEK.get("evaluated_at")
        self.conf["endNth"] = self.endNth


class _Pagination(Response):
    def __init__(self, opts, conf, json, url, cb):
        super().__init__(opts, conf, json, url, cb)

    def stop(self):
        self.cb(None, self)

    def next(self, opts):
        if not self.isNext:
            self.cb(None, self)
        else:
            self.cp_params(self.opts, opts)
            Pagination.pagination(self.opts, self.conf, self.cb)


class _PaginationP(Response):
    def __init__(self, opts, conf, json, url):
        super().__init__(opts, conf, json, url, lambda: None)

    async def next(self, opts):
        if not self.isNext:
            return None
        else:
            self.cp_params(self.opts, opts)
            return await Pagination.pagination_p(self.opts, self.conf)


class Pagination:

    @staticmethod
    def pagination(opts, conf, cb):

        url, err = None, None
        try:
            url = Util.make_url(opts, conf)
        except Exception as err2:
            err = err2

        if err:
            cb(err, None)
        else:
            def func_cb(_err, _json):
                nonlocal cb, conf, opts, url
                if not apis[conf["path_name"]][conf.get("method") or "get"].get("pagination"):
                    cb(_err, _json)
                else:
                    pagination = _Pagination(opts, conf, _json, url, cb)
                    if conf.get("getAll"):
                        conf["getAll"]((pagination.json or None), lambda: pagination.next(opts),
                                       lambda: pagination.stop(), pagination)
                    elif conf.get("getAllSync"):
                        conf["getAllSync"]((pagination.json or None), lambda: pagination.next(opts),
                                       lambda: pagination.stop(), pagination)
                    else:
                        cb(None, pagination.json)

            Request.request(url, opts, conf, func_cb)

    @staticmethod
    async def pagination_p(opts, conf):
        url = Util.make_url(opts, conf)

        r = await Request.request_p(url, opts, conf)

        try:
            json = r.json()
        except:
            return r

        if not apis[conf["path_name"]][conf.get("method") or "get"].get("pagination"):
            return json
        else:
            pagination = _PaginationP(opts, conf, json, url)
            if conf.get("getAll"):
                is_stop = await conf["getAll"](pagination.json, pagination)
                if is_stop or not pagination.isNext:
                    return json
                else:
                    return await pagination.next(opts)

            elif conf.get("getAllSync"):
                is_stop = conf["getAllSync"](pagination.json, pagination)
                if is_stop or not pagination.isNext:
                    return json
                else:
                    return await pagination.next(opts)
            else:
                return json
