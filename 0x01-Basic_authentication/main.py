#!/usr/bin/env python3

import base64
from api.v1.auth.basic_auth import BasicAuth
from models.user import User

user_email = "ahmed@gmail.com"
user_clear_pwd = "jiawdafawef"
user = User()
user.email = user_email
user.password = user_clear_pwd
print("New user: {} / {}".format(user.id, user.display_name()))
user.save()

basic_clear = "{}:{}".format(user_email, user_clear_pwd)
print("Basic Base64: {}".format(base64.b64encode(basic_clear.encode('utf-8')).decode("utf-8")))
