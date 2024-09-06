#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Creaet Time    : 2022/5/12 17:09 
# @File           : compute.py
# @IDE            : PyCharm
# @desc           : 精准计算
from decimal import Decimal
from typing import Union


class Compute:

    @staticmethod
    def add(precision: int, *args: Union[float, Decimal]) -> float:
        """
        相加
        :param precision: 精度
        """
        result = 0
        for i in args:
            if i is None:
                i = 0
            result += Decimal(str(i))
        if precision == -1:
            return float(result)
        return round(float(result), precision)

    @staticmethod
    def subtract(precision: int, *args: Union[float, Decimal]) -> float:
        """
        相减
        :param precision: 精度
        """
        if args[0] is None:
            start = 0
        else:
            start = args[0]
        result = Decimal(str(start))
        for i in args[1:]:
            if i is None:
                i = 0
            result -= Decimal(str(i))
        if precision == -1:
            return float(result)
        return round(float(result), precision)

    @staticmethod
    def divide(precision: int, *args: Union[float, Decimal]) -> float:
        """
        除法
        :param precision: 精度
        """
        result = Decimal(str(args[0]))
        for i in args[1:]:
            result = result / Decimal(str(i))
        if precision == -1:
            return float(result)
        return round(float(result), precision)

    @staticmethod
    def multiply(precision: int, *args: Union[float, Decimal]) -> float:
        """
        乘法
        :param precision: 精度
        """
        result = Decimal(str(1))
        for i in args:
            if i is None:
                i = 1
            result = result * Decimal(str(i))
        if precision == -1:
            return float(result)
        return round(float(result), precision)
