#! /usr/bin/env python3

from calendar import timegm
from datetime import datetime, timedelta

from jose import jwt

secret_key = "super-secret"
algorithm = "HS256"

user_id = 'a49b436a-d0b3-4e3e-84e5-ac9204a33042'
now = timegm(datetime.utcnow().utctimetuple())
exp = timegm((datetime.utcnow() + timedelta(minutes=50)).utctimetuple())

data = {
    'fresh': False,
    'iat': now,
    'jti': 'cf60f579-1cf8-4ca3-8d46-f19e629832d4',
    'type': 'access',
    'sub': user_id,
    'nbf': now,
    'exp': exp,
    'role': 'admin'
}
token = jwt.encode(data, secret_key, algorithm)
print(token)
