AES_SECRET_KEY = 'pnc3976myptcjmgp'

JWT_SECRET_KEY = "tin592ojcQzWr701PNCxbt"

ROUTES_PREFIX = "mypt-profile-api/v1/"

MIDDLEWARE_APPLIED_FOR_ROUTES = {
    "authenusermiddleware": [
        "/" + ROUTES_PREFIX + "health",
        "/" + ROUTES_PREFIX + "employee",
        "/" + ROUTES_PREFIX + "emp-checkin",
        "/" + ROUTES_PREFIX + "news",
        "/" + ROUTES_PREFIX + "home-banner",
        "/" + ROUTES_PREFIX + "get-notis-home",
        "/" + ROUTES_PREFIX + "get-profile-info",
    ]
}

