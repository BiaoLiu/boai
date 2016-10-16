# coding: utf-8
import uuid

def get_uuid():
    return str(uuid.uuid1()).replace('-', '')
