apis = {

    "/articles/recent": {
        "get": {
            "pagination": True,
            "by_page": True
        }
    },

    "/articles/popular": {
        "get": {
            "pagination": True,
            "by_page": True
        }
    },

    "/users/user_id/articles/public": {
        "get": {
            "pagination": True,
            "user_id": 'path'
        }
    },

    "/me/articles/public": {
        "get": {
            "auth": True,
            "pagination": True
        }
    },

    "/articles/article_id": {
        "get": {
            "article_id": 'path'
        }
    },

    "/articles/article_id/alistoken": {
        "get": {
            "article_id": 'path'
        }
    },

    "/articles/article_id/likes": {
        "get": {
            "article_id": 'path'
        }
    },

    "/me/articles/article_id/like": {
        "get": {
            "auth": True,
            "article_id": 'path'
        },
        "post": {
            "auth": True,
            "article_id": 'path'
        }
    },

    "/me/articles/article_id/public": {
        "get": {
            "auth": True,
            "article_id": 'path'
        },
        "put": {
            "auth": True,
            "article_id": 'path',
            "article": 'body'
        }
    },

    "/me/articles/article_id/fraud": {
        "post": {
            "auth": True,
            "article_id": 'path'
        }
    },

    "/me/articles/article_id/pv": {
        "post": {
            "auth": True,
            "article_id": 'path'
        }
    },

    "/me/articles/article_id/images": {
        "post": {
            "auth": True,
            "article_id": 'path',
            "ArticleImage": 'body',
            "Content-Type": 'header'
        }
    },

    "/me/articles/article_id/public/unpublish": {
        "put": {
            "auth": True,
            "article_id": 'path'
        }
    },

    "/me/articles/article_id/public/republish": {
        "put": {
            "auth": True,
            "article_id": 'path'
        }
    },

    "/me/articles/article_id/public/edit": {
        "get": {
            "auth": True,
            "article_id": 'path'
        }
    },

    "/me/articles/public/article_id/edit": {
        "get": {
            "auth": True,
            "article_id": 'path'
        }
    },

    "/me/articles/article_id/drafts": {
        "get": {
            "auth": True,
            "article_id": 'path'
        },
        "put": {
            "auth": True,
            "article_id": 'path',
            "article": 'body'
        }

    },

    "/me/articles/article_id/drafts/publish": {
        "put": {
            "auth": True,
            "article_id": 'path'
        }

    },

    "/me/articles/drafts": {
        "get": {
            "auth": True,
            "pagination": True
        },
        "post": {
            "auth": True,
            "article": 'body'
        }
    },

    "/users/user_id/info": {
        "get": {
            "user_id": 'path'
        }
    },

    "/me/info": {
        "get": {
            "auth": True
        },
        "put": {
            "auth": True,
            "user_info": 'body'
        }
    },

    "/me/info/icon": {
        "post": {
            "auth": True,
            "icon": 'body',
            "Content-Type": 'header'
        }
    },

    "/me/wallet/balance": {
        "get": {
            "auth": True
        }
    },

    "/me/wallet/tip": {
        "post": {
            "auth": True
        }
    },

    "/articles/article_id/comments": {
        "get": {
            "article_id": 'path',
            "pagination": True
        }
    },

    "/comments/comment_id/likes": {
        "get": {
            "comment_id": 'path'
        }
    },

    "/me/articles/article_id/comments": {
        "post": {
            "auth": True,
            "article_id": "path",
            "comment": "body"
        }
    },

    "/me/articles/article_id/comments/likes": {
        "get": {
            "auth": True,
            "article_id": 'path'
        }
    },

    "/me/comments/comment_id": {
        "delete": {
            "auth": True,
            "comment_id": "path"
        }
    },

    "/me/comments/comment_id/likes": {
        "post": {
            "auth": True,
            "comment_id": 'path'
        }
    },

    "/me/notifications": {
        "get": {
            "auth": True,
            "pagination": True
        }
    },

    "/me/unread_notification_managers": {
        "get": {
            "auth": True
        },
        "put": {
            "auth": True
        }
    },

    "/topics": {
        "get": {
        }
    },

    "/search/articles": {
        "get": {
            "pagination": True,
            "by_page": True
        }
    },

    "/search/users": {
        "get": {
            "pagination": True,
            "by_page": True
        }
    },

    "/articles/article_id/supporters": {
        "get": {
            "article_id": 'path'
        }
    }
}
