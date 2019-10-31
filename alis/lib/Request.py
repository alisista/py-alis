import asyncio
import json as js
import requests
from pprint import pprint
from promise import Promise
from .apis import apis
from .Util import Util
from .Cognito import Cognito


class Request:

    @staticmethod
    def _auth(conf, cb):
        headers = {}
        def func_token(token):
            if not token:
                raise ValueError("the wrong username or password")
            else:
                nonlocal headers, conf, cb
                headers["Authorization"] = token["id_token"]
                conf["id_token"] = token["id_token"]
                conf["refresh_token"] = token["refresh_token"]
                conf["token_source"] = "cognito"
                cb(headers)
        Cognito.get_tokens(conf, func_token)

    @staticmethod
    def auth(conf, cb):
        headers = {}
        if not apis[conf["path_name"]][conf.get("method") or "get"].get("auth"):
            cb(headers)
        elif conf.get("id_token"):
            headers["Authorization"] = conf["id_token"]
            conf["token_source"] = "user"
            cb(headers)
        else:
            if not conf.get("username"):
                raise ValueError("username is required")
            else:
                if conf.get("refresh_token"):
                    def func_token(tokens):
                        nonlocal headers, conf, cb
                        if tokens:
                            headers["Authorization"] = tokens.get("id_token")
                            conf["id_token"] = tokens.get("id_token")
                            conf["refresh_token"] = tokens.get("refresh_token")
                            conf["token_source"] = "cognito"
                            cb(headers)
                        else:
                            Request._auth(conf, cb)
                    Cognito.refresh_token(conf, func_token)
                else:
                    Request._auth(conf, cb)

    @staticmethod
    async def auth_p(conf):
        headers = {}
        if apis[conf["path_name"]][conf.get("method") or "get"].get("auth"):
            if conf.get("id_token"):
                headers["Authorization"] = conf["id_token"]
                conf["token_source"] = "user"
            else:
                if not conf.get("username"):
                    raise ValueError("username is required")
                else:
                    tokens = {}
                    token_source = None
                    if conf.get("refresh_token"):
                        tokens = await Cognito.refresh_token_p(conf)
                        token_source = "cognito"
                        tokens = tokens.get()
                        # tokens = tokens.get() or Cognito.get_cache(conf)
                    # else:
                    #     tokens = tokens or Cognito.get_cache(conf)

                    if tokens:
                        headers["Authorization"] = tokens["id_token"]
                        conf["id_token"] = tokens["id_token"]
                        conf["refresh_token"] = tokens["refresh_token"]
                        conf["token_source"] = token_source or "cache"
                    elif not tokens and not conf.get("password"):
                        raise KeyError("password is required")
                    else:
                        tokens = await Cognito.get_tokens_p(conf)
                        if not tokens.get():
                            raise ValueError("the wrong username or password")
                        else:
                            headers["Authorization"] = tokens.get()["id_token"]
                            conf["id_token"] = tokens.get()["id_token"]
                            conf["refresh_token"] = tokens.get()["refresh_token"]
                            conf["token_source"] = "cognito"
        return headers

    @staticmethod
    def request(url, opts, conf, cb):
        method = conf.get("method") or "get"
        options = {}

        def func_headers(x):
            nonlocal conf, opts, options, cb

            if conf.get("id_token"):
                x["Authorization"] = conf["id_token"]
            Util.add_headers(x, opts, conf)

            options = {
                "url": str(url.pathname),
                "headers": x
            }

            Util.add_body(options, opts, conf)

            if not options.get("json"):
                r = requests.__getattribute__(method)(url=options["url"],
                    params=url.params, headers=options["headers"])
            else:
                r = requests.__getattribute__(method)(url=options["url"],
                    params=url.params, headers=options["headers"], data=js.dumps(options["json"]).encode('utf-8'))

            json = None
            err = None

            try:
                json = r.json()
            except:
                json = r

            try:
                r.raise_for_status()
            except requests.exceptions.HTTPError as errh:
                print("Http Error:", errh)
                err = errh
            except requests.exceptions.ConnectionError as errc:
                print("Error Connecting:", errc)
                err = errc
            except requests.exceptions.Timeout as errt:
                print("Timeout Error:", errt)
                err = errt
            except requests.exceptions.RequestException as errr:
                print("Request Error:", errr)
                err = errr

            if r.status_code != 200:
                if r.status_code == 401 and not conf.get("retry"):
                    if conf.get("refresh_token") and conf.get("username"):
                        def func_token(tokens):
                            nonlocal conf
                            if tokens:
                                conf["retry"] = True
                                conf["id_token"] = tokens["id_token"]
                                conf["refresh_token"] = tokens["refresh_token"]
                                conf["token_source"] = "cognito"
                                Request.request(url, opts, conf, cb)
                            else:
                                conf["refresh_token"] = None
                                conf["id_token"] = None
                                cb(json, None)
                        Cognito.refresh_token(conf, func_token)
                    else:
                        conf["refresh_token"] = None
                        conf["id_token"] = None
                        conf["retry"] = True
                        Request.request(url, opts, conf, cb)
                else:
                    cb(json, None)
            else:
                cb(err, json)
        Request.auth(conf, func_headers)

    @staticmethod
    async def request_p(url, opts, conf):

        method = conf.get("method") or "get"
        headers = await Request.auth_p(conf)
        Util.add_headers(headers, opts, conf)
        options = {
            "url": str(url.pathname),
            "headers": headers
        }
        Util.add_body(options, opts, conf)

        def call_requests(resolve):

            if not options.get("json"):
                r = requests.__getattribute__(method)(url=options["url"],
                    params=url.params, headers=options["headers"])
            else:
                r = requests.__getattribute__(method)(url=options["url"],
                    params=url.params, headers=options["headers"], data=js.dumps(options["json"]).encode('utf-8'))
            resolve(r)

        r = await Promise(lambda resolve, reject: call_requests(resolve))

        err = None
        try:
            r.raise_for_status()
        except requests.exceptions.HTTPError as errh:
            print("Http Error:", errh)
            err = errh
        except requests.exceptions.ConnectionError as errc:
            print("Error Connecting:", errc)
            err = errc
        except requests.exceptions.Timeout as errt:
            print("Timeout Error:", errt)
            err = errt
        except requests.exceptions.RequestException as errr:
            print("Request Error:", errr)
            err = errr

        if err:
            if r.status_code == 401 and not conf.get("retry"):
                if conf.get("refresh_token") and conf.get("username"):
                    refresh_tokens = await Cognito.refresh_token_p(conf)
                    if not refresh_tokens:
                        conf["retry"] = True
                        conf["id_token"] = refresh_tokens["id_token"]
                        conf["refresh_token"] = refresh_tokens["refresh_token"]
                        conf["token_source"] = "cognito"
                        return await Request.request_p(url, opts, conf)
                    else:
                        conf["refresh_token"] = None
                        conf["id_token"] = None
                        raise err
                else:
                    conf["refresh_token"] = None
                    conf["id_token"] = None
                    conf["retry"] = True
                    return await Request.request_p(url, opts, conf)
            else:
                raise err

        return r
