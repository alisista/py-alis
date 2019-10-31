# ALIS API Python Client

[![CircleCI](https://circleci.com/gh/alisista/py-alis/tree/master.svg?style=svg)](https://circleci.com/gh/alisista/py-alis/tree/master)

This is an API Python client of [alis.to](https://alis.to). The original code ([ALIS API Node.js Client](https://github.com/alisista/alis))
was written by [OK Rabbit](https://github.com/ocrybit) ([@ocrybit](https://twitter.com/ocrybit)) and rewritten in Python by [hoosan](https://github.com/hoosan)([@hoosan16](https://twitter.com/hoosan16)).

## ALIS API made simple with syntax sugar

The simplest call looks like this.

```python
Alis.api("/articles/recent", lambda err, json: pprint(json))
```

The same call promisified, simply replace `api` by `api_p`.

```python
# with the promise-based calls, you are free from callback hell
json = Alis.api_p("/articles/recent", {'article_id': '2xANPLY5QrN1'}, {"method": "GET"})
```

Another example to get all the articles an authenticated user has published on ALIS with a promisified call.
It loops through all the articles successively paginating till it reaches the end, but you can put some logics between each call with a `getAll/getAllSync` function defined to make pagination easier. 

This time the example uses an `async/await` wrapper function to make it work like a synchronous code.

```python
page = 0
async def get_all_p(json, obj):
    nonlocal page
    print(f"{obj.itemCount} articles fetched from {obj.startNth}th to {obj.endNth}th.")
    page += 1
    for i, item in enumerate(json["Items"]):
        print(f"[{obj.startNth+i}]{item['title']}")
    if page == 3:
        return True
    else:
        return False
Alis.api_p("/me/articles/public", {"limit": 2}, {"username": "xxxxx", "password": "xxxxx", "getAll": get_all_p})
```

## Table of contents

- [Installation](#installation)
- [Available Calls](#available-calls)
- [Authentication](#authentication)
- [Syntax Sugar](#syntax-sugar)
- [Links](#links)
- [Contributors](#contributors)


---


## Installation

The `pip` installation is available.

```
$ pip install alis
```

If you wish to use conda, install pip before alis so as not to mess up libraries.

```
$ conda install pip
$ pip install alis
```


---


## Available Calls

Refer to the official ALIS API documentation located [here](https://alisproject.github.io/api-docs/).

All you have to do to make a call is to remove `{}` from each pathname of the call and put it as the first argument.
Also specify the request method in the third argument when it's not `GET`.

When authentication is needed, pass your `username` and `password` to the third argument as well.

Arguments are

`1st` pathname of ALIS API; e.g., `"/me/articles/public"`.

`2nd` parameters specified in the API document to pass to the API call.

`3rd` anything else specific to this library

`4th` the last callback function (not for promise-based calls)

You can omit the second and third argument when not required and put the last callback function as the second argument.
However, you cannot omit the second argument when you need to specify the third argument.

Some examples.

[GET] /articles/{article_id}
```python
Alis.api("/articles/article_id", {"articles_id": "2xANPLY5QrN1"}, {}, lambda err, json: pprint(json))
```
[POST] /me/articles/{article_id}/like
```python
Alis.api("/me/articles/article_id/like", {"article_id": "2xANPLY5QrN1"}, {"method": "POST", "username": "your_username", "password": "your_password"})
```

Note that some `POST` and `PUT` API calls don't return anything back when successful, in that case this library returns `<Response [200]>` to indicate a successful operation.

---

## Authentication

ALIS uses [Amazon Cognito](https://aws.amazon.com/cognito/) to authenticate users but this library handles that in the background for you. You just need to pass your `username` and `password`, then it authenticates you through the complicated process and stores the tokens in a temporary file, it automagically refreshes your tokens when they are expired.

There are 3 ways to make API calls with authentication.

1. pass `username` and `password`
```python
Alis.api("/me/info", {}, {"username": "your_username", "password": "your_password"}, lambda err, json: pprint(json))
```
2. directly pass `id_token` obtained by authentication (optionally with `username`)
```python
Alis.api("/me/info", {}, {"id_token": "your_id_token"}, lambda err, json: pprint(json))
```
3. pass `refresh_token` and `username` (for some weired reasons)
```python
Alis.api("/me/info", {}, {"refresh_token": "your_refresh_token", "username": "your_username"}, lambda err, json: pprint(json))
```
Note that it's a good idea to always pass your `username` since both authenticating and refreshing operations require `username` to be done automatically.

---

## Syntax Sugar

Manually paginating through articles and comments might be pain in the ass, so this library made it simpler for you.

You can specify a `getAll` function to the third argument to make the call automatically go to the next page till it reaches the end. Use `next` and `stop` functions given back to you inside the `getAll` function to navigate.

Do something asynchronous and call `next` to get the next page or `stop` to intercept the loop and finish the operation with the last callback function.

The forth object returned to you contains some useful information for pagination such as `startNth`, `endNth`, `itemCount`, `isNext`. `startNth` and `endNth` are not zero-based index but they count from 1 like ordinal numbers.

```python
page = 0
def get_all(json, next, stop, obj):
    nonlocal page
    print(f"{obj.itemCount} articles fetched from {obj.startNth}th to {obj.endNth}th.")
    page += 1
    for i, item in enumerate(json["Items"]):
        print(f"[{obj.startNth+i}]{item['title']}")
    # stop the calls when it's on the 3rd page so the maximum articles to get will be 30
    if page == 3:
        stop()
    else:
        next()
Alis.api("/articles/popular", {"limit": 10}, {"method": "GET", "getAll": get_all}, lambda err, json: print("This is the last callback function called when everything is done.")
```

## Links

- [ALIS API Documentation](https://alisproject.github.io/api-docs/)
- [ALIS WebService](https://alis.to)
- [ALIS Unofficial DISCORD Hacker Club](https://discordapp.com/invite/zKKNtUe)
- [ALIS SEARCH](https://alisista.com)
- [ALIS Articles Miner (ALIS過去記事マイナー)](https://alis.ocrybit.com)
- [ALIS API Node.js Client](https://github.com/alisista/alis)


## Contributors

- Original code (Node.js):  [OK Rabbit](https://github.com/ocrybit) ([@ocrybit](https://twitter.com/ocrybit))
- Translator (from Node.js to Python): [hoosan](https://github.com/hoosan)([@hoosan16](https://twitter.com/hoosan16))