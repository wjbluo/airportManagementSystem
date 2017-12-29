# -*- coding: utf-8 -*-
import hashlib

from django.conf import settings

def transfor_md5(password):
    password_m = hashlib.md5(password.encode("utf-8"))
    return password_m.hexdigest()


# print(transfor_md5('admin'))

# d1bd83a33f1a841ab7fda32449746cc4
# c81e728d9d4c2f636f067f89cc14862c

