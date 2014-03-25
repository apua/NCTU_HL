# -*- coding=utf8 -*-

from django.contrib import admin

import inspect
import shopping_cart.models as M
from django.db.models.base import ModelBase

for name, member in inspect.getmembers(M):
    if inspect.isclass(member) and isinstance(member, ModelBase):
        admin.site.register(member)
