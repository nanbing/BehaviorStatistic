# -*- coding:utf-8 -*-
from db import db

def trac_behavior(action):
    db.increase(action)
