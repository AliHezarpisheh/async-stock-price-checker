from enum import Enum


class AuthScheme(Enum):
    BASIC = "Basic"
    BEARER = "Bearer"
    DIGEST = "Digest"
