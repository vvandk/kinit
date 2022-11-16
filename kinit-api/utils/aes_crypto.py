import base64
from Crypto.Cipher import AES  # 安装：pip install pycryptodome


# 密钥（key）, 密斯偏移量（iv） CBC模式加密
# base64 详解：https://cloud.tencent.com/developer/article/1099008

_key = '0CoJUm6Qywm6ts68'  # 自己密钥


def aes_encrypt(data: str):
    """
    加密
    """
    vi = '0102030405060708'
    pad = lambda s: s + (16 - len(s) % 16) * chr(16 - len(s) % 16)
    data = pad(data)
    # 字符串补位
    cipher = AES.new(_key.encode('utf8'), AES.MODE_CBC, vi.encode('utf8'))
    encrypted_bytes = cipher.encrypt(data.encode('utf8'))
    # 加密后得到的是bytes类型的数据
    encode_strs = base64.urlsafe_b64encode(encrypted_bytes)
    # 使用Base64进行编码,返回byte字符串
    # 对byte字符串按utf-8进行解码
    return encode_strs.decode('utf8')


def aes_decrypt(data):
    """
    解密
    """
    vi = '0102030405060708'
    data = data.encode('utf8')
    encode_bytes = base64.urlsafe_b64decode(data)
    # 将加密数据转换位bytes类型数据
    cipher = AES.new(_key.encode('utf8'), AES.MODE_CBC, vi.encode('utf8'))
    text_decrypted = cipher.decrypt(encode_bytes)
    unpad = lambda s: s[0:-s[-1]]
    text_decrypted = unpad(text_decrypted)
    # 补位
    text_decrypted = text_decrypted.decode('utf8')
    return text_decrypted


if __name__ == '__main__':
    _data = '16658273438153332588-95YEUPJR'  # 需要加密的内容

    enctext = aes_encrypt(_data)
    print(enctext)

    # enctext = "Wzll1oiVs9UKAySY1-xSy_CbrZmelVwyqu8P0CZTrrc="
    # _text_decrypted = aes_decrypt(_key, enctext)
    # print(_text_decrypted)
