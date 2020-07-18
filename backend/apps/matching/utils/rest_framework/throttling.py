from rest_framework.throttling import UserRateThrottle


class UserMinRateThrottle(UserRateThrottle):
    scope = "user_min"


class UserHRateThrottle(UserRateThrottle):
    scope = "user_h"


class UserDayRateThrottle(UserRateThrottle):
    scope = "user_day"
