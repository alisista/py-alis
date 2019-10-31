import asyncio
from pprint import pprint
from alis.lib.apis import apis
from alis.lib.Call import Call

def api(path, *args):
    args = list(args)
    args.append({"path_name": path})
    Call.call(args)


def api_p(path, *args):
    args = list(args)
    args.append({"path_name": path, "ispromise": True})
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(Call.call_p(args))

# test 1: "/articles/recent"
# api("/articles/recent", {}, {"method": "GET"}, lambda err, json: pprint(json))

# test 2: "/articles/recent" (promise)
# pprint(api_p("/articles/recent", {'article_id': '2xANPLY5QrN1'}, {"method": "GET"}))

# test 3: "/articles/popular" with get_all function
# page = 0
# def get_all(json, next, stop, obj):
#     nonlocal page
#     print(f"{obj.itemCount} articles fetched from {obj.startNth}th to {obj.endNth}th.")
#     page += 1
#     for item in json["Items"]:
#         print(item)
#     if page == 3:
#         stop()
#     else:
#         next()
# api("/articles/popular", {"limit": 10}, {"method": "GET", "getAll": get_all}, lambda err, json: None)

# test 4: "/articles/popular" with get_all function (promise)
# page = 0
# async def get_all_p(json, obj):
#     nonlocal page
#     print(f"{obj.itemCount} articles fetched from {obj.startNth}th to {obj.endNth}th.")
#     page += 1
#     for item in json["Items"]:
#         print(item)
#     if page == 3:
#         return True
#     else:
#         return False
# api_p("/articles/popular", {"limit": 10}, {"method": "GET", "getAll": get_all_p})

# test 5: "/me/info"
# api("/me/info", {}, {"username": "xxxxx", "password": "xxxxx"}, lambda err, json: pprint(json))

# test 6: "/me/info" (promise)
# json = api_p("/me/info", {}, {"username": "xxxxx", "password": "xxxxx"})
# pprint(json)

# test 7: "/users/user_id/articles/public"
# api("/users/user_id/articles/public", {"user_id": "fukurou"}, {}, lambda err, json: pprint(json))

# test 8: "/users/user_id/articles/public" with get_all_p (primise)
# page = 0
# async def get_all_p(json, obj):
#     nonlocal page
#     print(f"{obj.itemCount} articles fetched from {obj.startNth}th to {obj.endNth}th.")
#     page += 1
#     for i, item in enumerate(json["Items"]):
#         print(f"[{obj.startNth+i}]{item['title']}")
#     if page == 100:
#         return True
#     else:
#         return False
# Alis.api_p("/users/user_id/articles/public", {"limit": 2, "user_id": "fukurou"}, {"getAll": get_all_p})

# test 9: "/me/articles/public" with get_all
# page = 0
# def get_all(json, next, stop, obj):
#     nonlocal page
#     print(f"{obj.itemCount} articles fetched from {obj.startNth}th to {obj.endNth}th.")
#     page += 1
#     for i, item in enumerate(json["Items"]):
#         print(f"[{obj.startNth+i}]{item['title']}")
#     if page == 100:
#         stop()
#     else:
#         next()
# Alis.api("/me/articles/public", {"limit": 3}, {"username": "xxxxx", "password": "xxxxx", "getAll": get_all}, lambda *args: None)

# test 10: "/articles/article_id"
# Alis.api("/articles/article_id", {"article_id": '2xANPLY5QrN1'}, {}, lambda err, json: pprint(json))

# test 11: "/articles/article_id/likes"
# Alis.api("/articles/article_id/likes", {"article_id": '2xANPLY5QrN1'}, {}, lambda err, json: pprint(json))

# test 12: "/me/articles/article_id/like"
# Alis.api("/me/articles/article_id/like", {"article_id": '2xANPLY5QrN1'}, {"username": "xxxxx", "password": "xxxxx"}, lambda err, json: pprint(json))

# test 13: "/me/articles/article_id/images"
# import base64
# file_path = "xxxxx.png"
# file = base64.b64encode(open(file_path, 'rb').read()).decode('utf-8')
# Alis.api("/me/articles/article_id/images",
#          {"article_id": "anLOqAJDpdqV", "ArticleImage": {"article_image": file}, 'Content-Type': 'image/png'},
#          {"method": "POST", "username": "xxxxx", "password": "xxxxx"},
#          lambda err, res: pprint(res))

# test 14: "/me/articles/article_id/public/unpublish"
# Alis.api("/me/articles/article_id/public/unpublish",
#          {"article_id": 'xxxxxxxxxxxx'},
#          {"method": "PUT", "username": "xxxxx", "password": "xxxxx"},
#           lambda err, res: pprint(res.url))

# test 15: "/me/info/icon"
# import base64
# file_path = "xxxxx.png"
# file = base64.b64encode(open(file_path, 'rb').read()).decode('utf-8')
# Alis.api("/me/info/icon", {"icon": {"icon_image": file}, 'Content-Type': 'image/png'},
#           {"method": "POST", "username": "xxxxx", "password": "xxxxx"},
#           lambda err, res: pprint(res))

# test 16: "/articles/article_id/comments"
# Alis.api("/articles/article_id/comments", {"article_id": 'K8Dz1j8OqNDr'}, {"method": "GET"}, lambda err, res: pprint(res))

# test 17: "/me/articles/article_id/comments"
# Alis.api("/me/articles/article_id/comments",
#          {"article_id": 'xxxxxxxxxxxx', "comment": {"text": "APIクライアントからのテスト投稿"}},
#          {"method": "POST", "username": "xxxxx", "password": "xxxxx"},
#          lambda err, res: pprint(res))

# test 18 "/me/wallet/balance"
# Alis.api("/me/wallet/balance", {}, {"username": "xxxxx", "password": "xxxxx"}, lambda err, res: pprint(res))

# test 19 "/me/unread_notification_managers"
# Alis.api("/me/unread_notification_managers", {}, {"username": "xxxxx", "password": "xxxxx"}, lambda err, res: pprint(res))

# test 20 "/me/notifications"
# Alis.api("/me/notifications", {}, {"username": "xxxxx", "password": "xxxxx "}, lambda err, res: pprint(res))

# test 20: "/articles/article_id/supporters"
# api("/articles/article_id/supporters", {"article_id": "2jDOBZMXeWlv"}, {}, lambda err, res: pprint(res))



