# coding: utf-8
from enum import Enum, unique


@unique
class OrderStatus(Enum):
    UnPaid = 0
    Paid = 1
    Refund = 2

