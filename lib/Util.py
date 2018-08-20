import types
from .apis import apis

ep = "https://alis.to/api"


class URL:

    def __init__(self, pathname, api):
        self.pathname = pathname
        self.params = {}
        self.api = api

    def set_params(self, key, option):
        if not self.api.get(key):
            self.params[key] = option


class Util:

    @staticmethod
    def make_url(opts, conf):
        method = conf.get("method") or 'get'
        api = apis.get(conf.get('path_name'))
        if not api:
            raise KeyError("api call doesn't exist")
        api = api.get(method)
        if not api:
            raise KeyError("the wrong method")
        path_name = []
        for v in conf["path_name"].split("/"):
            if api.get(v) == "path":
                if not opts.get(v):
                    raise KeyError(f"{v} is required")
                else:
                    path_name.append(opts.get(v))
            else:
                path_name.append(v)
        url = URL(ep, api)
        url.pathname += "/".join(path_name)

        for k in opts:
            if opts.get(k):
                url.set_params(k, opts[k])
        return url

    @staticmethod
    def validate(args):
        opts, conf, cb = [], [], []
        args = args[0]
        call_conf = args.pop()
        min_args = 3
        if call_conf.get('ispromise'):
            min_args -= 1

        if len(args) > min_args:
            raise ValueError("too many arguments")
        else:
            if not call_conf.get('ispromise'):
                cb = args.pop()
                if not isinstance(cb, types.FunctionType):
                    raise TypeError("callback must be a function")
            if len(args) != 0:
                opts = args.pop(0) or {}
            if len(args) != 0:
                conf = args.pop(0) or {}

            opts = opts or {}
            if not isinstance(opts, dict):
                raise TypeError("first argument must be a dictionary")

            conf = conf or {}
            if not isinstance(conf, dict):
                raise TypeError("second argument must be a dictionary")

            for k in conf:
                if k not in ["method", "id_token", "getAll", "getAllSync", "username", "password", "refresh_token"]:
                    raise ValueError(f"unknown parameter {k}")

            for k in call_conf:
                conf[k] = call_conf[k]

            conf["method"] = (conf.get("method") or "get").lower()
            return [opts, conf, cb]

    @staticmethod
    def add_body(options, opts, conf):
        api = apis[conf["path_name"]][conf.get("method") or "get"]
        for k in opts:
            if api.get(k) == "body":
                options["json"] = opts[k]
                break

    @staticmethod
    def add_headers(headers, opts, conf):
        api = apis[conf["path_name"]][conf.get("method") or "get"]
        for k in opts:
            if api.get(k) == "header":
                headers[k] = opts[k]

    @staticmethod
    def add_params(url, fields, values):
        for v in fields:
            if values.get(v):
                url.set_params(v, values[v])
