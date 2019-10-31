import asyncio
import json
import os
from promise import Promise
from warrant import Cognito as WarrantCognito

POOL_ID = 'ap-northeast-1_HNT0fUj4J'
POOL_REGION = 'ap-northeast-1'
CLIENT_ID = '2gri5iuukve302i4ghclh6p5rg'


class Cognito:

    @staticmethod
    def get_cognito_user(conf):
        username = conf['username']
        cognito = WarrantCognito(POOL_ID, CLIENT_ID, user_pool_region=POOL_REGION, username=username)
        return cognito

    @staticmethod
    def reg_tokens(session, conf, cb):
        tokens = {
            "username": conf["username"],
            "access_token": session.access_token,
            "id_token": session.id_token,
            "refresh_token": session.refresh_token
        }
        cb(tokens)

    @staticmethod
    def refresh_token(conf, cb):
        refresh_token = conf.get("refresh_token")
        cognito_user = Cognito.get_cognito_user(conf)
        cognito_user.refresh_token = refresh_token
        # memo: an anonymous function is used here in the original code
        try:
            cognito_user.renew_access_token()
            Cognito.reg_tokens(cognito_user, conf, cb)
        except:
            # too broad exception
            cb(None)

    @staticmethod
    async def refresh_token_p(conf):
        return Promise(lambda resolve, reject: Cognito.refresh_token(conf, resolve))

    @staticmethod
    def get_tokens(conf, cb):
        cognito_user = Cognito.get_cognito_user(conf)

        # memo: an anonymous function is used here in the original code
        try:
            password = conf["password"]
            cognito_user.authenticate(password=password)
            Cognito.reg_tokens(cognito_user, conf, cb)
        except:
            # too broad exception
            cb(None)

    @staticmethod
    async def get_tokens_p(conf):
        return Promise(lambda resolve, reject: Cognito.get_tokens(conf, resolve))
