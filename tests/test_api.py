from alis import alis
import pprint
import pytest

class TestArticlesRecent:

    def test_callback(self):
        def callback(err, json):
            # print(json)
            assert json.get("Items")
        alis.api("/articles/recent", {}, {"method": "GET"}, callback)
        
    def test_callback_by_page(self):
        def callback(err, json):
            # print(json)
            assert json.get("Items")
        alis.api("/articles/recent", {"page": 2}, {"method": "GET"}, callback)

    def test_promise(self):
        json = alis.api_p("/articles/recent")
        assert json.get("Items")

class TestArticlesPopular:

    def test_get_all(self):
        page = 0
        def get_all(json, next, stop, obj):
            nonlocal page
            # print(f"{obj.itemCount} articles fetched from {obj.startNth}th to {obj.endNth}th.")
            page += 1
            # for item in json["Items"]:
            #     print(item)
            if page == 3:
                stop()
            else:
                next()
        
        def callback(err, page):
            assert page.json.get("Items")

        alis.api("/articles/popular", {"limit": 10}, {"method": "GET", "getAll": get_all}, callback)

    def test_get_all_promise(self):
        page = 0
        async def get_all_p(json, obj):
            nonlocal page
            # print(f"{obj.itemCount} articles fetched from {obj.startNth}th to {obj.endNth}th.")
            page += 1
            # for item in json["Items"]:
            #     print(item)
            if page == 3:
                return True
            else:
                return False
        json = alis.api_p("/articles/popular", {"limit": 10}, {"method": "GET", "getAll": get_all_p})
        assert json.get("Items")


class TestInfo:

    def test_wrong_password_callback(self):
        def callback(err, json):
            pass
        with pytest.raises(ValueError, match='password'):
            alis.api("/me/info", {}, {"username": "test", "password": "test"}, callback)

    def test_wrong_password_promise(self):
        with pytest.raises(ValueError, match='password'):
            alis.api_p("/me/info", {}, {"username": "test", "password": "test"})

    # def test_info_callback(self):
    #     def callback(err, json):
    #         assert json.get('user_id')
    #     alis.api("/me/info", {}, {"username": 'test', "password": 'test'}, callback)

    def test_refresh_token_error_callback(self):
        def callback(err, json):
            pass
        with pytest.raises(ValueError):
            alis.api("/me/info", {}, {"username": 'test', "refresh_token": "test"}, callback)

    def test_refresh_token_error_promise(self):
        with pytest.raises(KeyError):
            alis.api_p("/me/info", {}, {"username": 'test', "refresh_token": "test"})

    def test_id_token_error_callback(self):
        def callback(err, json):
            pass
        with pytest.raises(ValueError):
            alis.api("/me/info", {}, {"username": 'test', "id_token": "test"}, callback)

    def test_id_token_error_promise(self):
        with pytest.raises(KeyError):
            alis.api_p("/me/info", {}, {"username": 'test', "id_token": "test"})

    def test_no_username_error_callback(self):
        def callback(err, json):
            pass
        with pytest.raises(ValueError):
            alis.api("/me/info", {}, {}, callback)

    def test_no_username_error_promise(self):
        with pytest.raises(ValueError, match="username"):
            alis.api_p("/me/info", {}, {})


class TestUsers:

    def test_user_id_articles_public_callback(self):
        def callback(err, json):
            assert json.get("Items")
        alis.api("/users/user_id/articles/public", {"user_id": "fukurou"}, {}, callback)
    
    def test_user_id_articles_public_callback_get_all(self):
        page = 0
        def get_all(json, next, stop, obj):
            nonlocal page
            page += 1
            next()
        def callback(err, json):
            nonlocal page
            assert page > 0
        alis.api("/users/user_id/articles/public", {"user_id": "fukurou", "limit": 10}, {"getAll": get_all}, callback)

    def test_user_id_articles_public_callback_get_all_sync(self):
        page = 0
        def get_all_sync(json, next, stop, obj):
            nonlocal page
            page += 1
            next()
        def callback(err, json):
            nonlocal page
            assert page > 0
        alis.api("/users/user_id/articles/public", {"user_id": "fukurou", "limit": 10}, {"getAllSync": get_all_sync}, callback)
 
    def test_user_id_articles_public_promise(self):
        json = alis.api_p("/users/user_id/articles/public", {"user_id": "fukurou"}, {})
        assert json.get('Items')
    
    def test_user_id_articles_public_promise_get_all(self):
        page = 0
        async def get_all_p(json, obj):
            nonlocal page
            page += 1
            return False
        alis.api_p("/users/user_id/articles/public", {"user_id": "fukurou", "limit": 10}, {"getAll": get_all_p})
        assert True

    def test_user_id_articles_public_promise_get_all_sync(self):
        page = 0
        async def get_all_sync_p(json, obj):
            nonlocal page
            page += 1
            return False
        alis.api_p("/users/user_id/articles/public", {"user_id": "fukurou", "limit": 10}, {"getAllSync": get_all_sync_p})
        assert True

class TestWrongAPI:

    def test_wrong_api_callback(self):
        def callback(err, json):
            assert err
        alis.api("/wrong/api", {}, {}, callback)
    
    def test_wrong_api_promise(self):
        with pytest.raises(KeyError, match="api call"):
            alis.api_p("/wrong/api")
