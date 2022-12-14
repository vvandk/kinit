#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Creaet Time    : 2022/10/9 17:09 
# @File           : tools.py
# @IDE            : PyCharm
# @desc           : 工具类

import datetime
import re
from typing import List, Union


def test_password(password: str) -> Union[str, bool]:
    """
    检测密码强度
    """
    if len(password) < 8 or len(password) > 16:
        return '长度需为8-16个字符,请重新输入。'
    else:
        for i in password:
            if 0x4e00 <= ord(i) <= 0x9fa5 or ord(i) == 0x20:  # Ox4e00等十六进制数分别为中文字符和空格的Unicode编码
                return '不能使用空格、中文，请重新输入。'
        else:
            key = 0
            key += 1 if bool(re.search(r'\d', password)) else 0
            key += 1 if bool(re.search(r'[A-Za-z]', password)) else 0
            key += 1 if bool(re.search(r"\W", password)) else 0
            if key >= 2:
                return True
            else:
                return '至少含数字/字母/字符2种组合，请重新输入。'


def list_dict_find(options: List[dict], key: str, value: any) -> Union[dict, None]:
    """
    字典列表查找
    """
    for item in options:
        if item.get(key) == value:
            return item
    return None


if __name__ == '__main__':
    # print(generate_invitation_code())
    print(int(datetime.datetime.now().timestamp()))
